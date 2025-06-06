#include <pqxx/pqxx>
#include <iostream>
#include <vector>
#include <thread>
#include <mutex>
#include <map>
#include "calculate.hpp"

#include <curl/curl.h>
#include <rapidjson/document.h>
#include <rapidjson/error/en.h>
#include <fstream>

double get_stock_price(const std::string &symbol)
{
  std::string api_key = read_secret("API_FINNHUB");
  CURL *curl = curl_easy_init();
  std::string readBuffer;
  double price = -1.0;

  if (curl)
  {
    std::string url = "https://finnhub.io/api/v1/quote?symbol=" + symbol + "&token=" + api_key;
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
    CURLcode res = curl_easy_perform(curl);
    curl_easy_cleanup(curl);

    if (res == CURLE_OK)
    {
      try
      {
        rapidjson::Document json_data;
        json_data.Parse(readBuffer.c_str());

        if (json_data.HasParseError())
        {
          std::cerr << "JSON parse error: "
                    << rapidjson::GetParseError_En(json_data.GetParseError())
                    << " (offset " << json_data.GetErrorOffset() << ")\n";
        }
        else if (json_data.HasMember("c") && json_data["c"].IsNumber())
        {
          price = json_data["c"].GetDouble();
        }
        else
        {
          std::cerr << "Missing or invalid 'c' field in JSON.\n";
        }
      }
      catch (const std::exception &e)
      {
        std::cerr << "Exception while parsing JSON: " << e.what() << std::endl;
      }
    }
    else
    {
      std::cerr << "Curl error: " << curl_easy_strerror(res) << std::endl;
    }
  }
  return price;
}

std::mutex price_mutex;

void fetch_price_task(const std::vector<std::pair<int, std::string>> &symbols,
                      std::map<int, double> &results,
                      size_t start, size_t end)
{
  for (size_t i = start; i < end; ++i)
  {
    int stock_id = symbols[i].first;
    std::string symbol = symbols[i].second;
    double price = get_stock_price(symbol);

    if (price > 0)
    {
      std::lock_guard<std::mutex> lock(price_mutex);
      results[stock_id] = price;
    }
    else
    {
      std::cerr << "Error: " << symbol << std::endl;
    }
  }
}

void fill_stock_data()
{
  try
  {
    std::string db_name = read_secret("POSTGRES_DB");
    std::string db_user = read_secret("POSTGRES_USER");
    std::string db_pass = read_secret("POSTGRES_PASSWORD");
    std::string db_host = "postgres";
    std::string db_port = "5432";

    std::string conn_str = "host=" + db_host + " port=" + db_port +
                           " dbname=" + db_name + " user=" + db_user +
                           " password=" + db_pass;

    pqxx::connection C(conn_str);
    if (!C.is_open())
    {
      std::cerr << "We can not conect to the database" << std::endl;
      return;
    }

    pqxx::work W(C);

    // 1. Részvénylista lekérése
    pqxx::result res = W.exec("SELECT id, link FROM stocks");
    std::vector<std::pair<int, std::string>> symbols;

    for (const auto &row : res)
    {
      int id = row["id"].as<int>();
      std::string symbol = row["link"].c_str();
      symbols.emplace_back(id, symbol);
    }

    // 2. Árlekérések párhuzamosan
    const size_t thread_count = std::min(size_t(8), symbols.size());
    std::vector<std::thread> threads;
    std::map<int, double> prices;

    size_t batch_size = (symbols.size() + thread_count - 1) / thread_count;

    for (size_t i = 0; i < thread_count; ++i)
    {
      size_t start = i * batch_size;
      size_t end = std::min(start + batch_size, symbols.size());
      threads.emplace_back(fetch_price_task, std::ref(symbols), std::ref(prices), start, end);
    }

    for (auto &t : threads)
    {
      t.join();
    }

    // 3. Frissítés adatbázisban
    for (const auto &[stock_id, price] : prices)
    {
      W.exec_params("UPDATE stocks SET price = $1 WHERE id = $2", price, stock_id);
    }

    W.commit();
  }
  catch (const std::exception &e)
  {
    std::cerr << "error  fill_stock_data: " << e.what() << std::endl;
  }
}
