#include <iostream>
#include <fstream>
#include <string>
#include <pqxx/pqxx>
#include <curl/curl.h>
#include <rapidjson/document.h>
#include <rapidjson/error/en.h>
#include <ctime>
#include <sstream>
#include <iomanip>
#include <cstdlib>
#include <future>
#include <vector>

std::string read_secret(const std::string &secret_name)
{
  std::ifstream file("/usr/local/bin/.env");
  if (!file.is_open())
  {
    std::cerr << "We can find this file: " << std::endl;
    return "";
  }

  std::string line;
  while (std::getline(file, line))
  {
    if (line.empty() || line[0] == '#')
      continue;

    size_t pos = line.find('=');
    if (pos != std::string::npos)
    {
      std::string key = line.substr(0, pos);
      std::string value = line.substr(pos + 1);

      key.erase(0, key.find_first_not_of(" \t"));
      key.erase(key.find_last_not_of(" \t") + 1);
      value.erase(0, value.find_first_not_of(" \t\""));
      value.erase(value.find_last_not_of(" \t\"") + 1);

      if (key.empty())
      {
        return "";
      }
      if (key == secret_name)
      {
        return value;
      }
    }
  }

  std::cerr << "Error can find this key: " << secret_name << std::endl;
  return "";
}

size_t WriteCallback(void *contents, size_t size, size_t nmemb, std::string *output)
{
  size_t totalSize = size * nmemb;
  output->append((char *)contents, totalSize);
  return totalSize;
}

double get_stock_price_in_database(const std::string &symbol, pqxx::work &txn)
{
  try
  {
    pqxx::result R = txn.exec_params(
        "SELECT price FROM stocks WHERE link = $1 LIMIT 1", symbol);

    if (!R.empty())
    {
      return R[0]["price"].as<double>();
    }
    else
    {
      std::cerr << "We don't have this symbol: " << symbol << std::endl;
    }
  }
  catch (const std::exception &e)
  {
    std::cerr << "Error to get_stock_price_in_database: " << e.what() << std::endl;
  }

  return -1.0;
}

struct Winner
{
  int id;
  double score;
  double winamount;
};

void calculate_wins_and_losses()
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
      std::cerr << "Connacon faild" << std::endl;
      return;
    }

    pqxx::work W(C);
    pqxx::result symbols = W.exec("SELECT DISTINCT symbol FROM bets");
    W.commit();

    std::vector<std::future<void>> futures;

    for (const auto &row : symbols)
    {
      std::string symbol = row["symbol"].as<std::string>();

      futures.push_back(std::async(std::launch::async,
                                   [conn_str, symbol]()
                                   {
                                     try
                                     {
                                       pqxx::connection local_conn(conn_str);
                                       pqxx::work local_txn(local_conn);

                                       double current_price = get_stock_price_in_database(symbol, local_txn);

                                       std::string query = "SELECT * FROM bets WHERE symbol = " + local_txn.quote(symbol);
                                       pqxx::result bets = local_txn.exec(query);

                                       std::string avg_query = "SELECT avgintervalum, avgtime, avgvolume FROM stocks WHERE link = " + local_txn.quote(symbol);
                                       pqxx::result stock_data = local_txn.exec(avg_query);

                                       if (stock_data.empty())
                                       {
                                         std::cerr << "Stock is empty: " << symbol << " for this symbol." << std::endl;
                                         return;
                                       }

                                       double avg_interval = stock_data[0]["avgintervalum"].as<double>();
                                       double avg_time = stock_data[0]["avgtime"].as<double>();
                                       double avg_volume = stock_data[0]["avgvolume"].as<double>();

                                       std::vector<Winner> winners;
                                       double total_score = 0.0;
                                       double allliqvidation = 0.0;

                                       for (const auto &bet : bets)
                                       {
                                         long current_time = std::time(nullptr);
                                         long deadline = bet["deadline"].as<long>();
                                         if (current_time > deadline)
                                         {
                                           continue;
                                         }
                                         double lower = bet["lower"].as<double>();
                                         double upper = bet["upper"].as<double>();
                                         double amount = bet["amount"].as<double>();
                                         int id = bet["id"].as<int>();
                                         double winamount = bet["winamount"].as<double>();
                                         double lossfee = bet["lossfee"].as<double>();
                                         long datenow = bet["datenow"].as<long>();
                                         if (current_price >= lower && current_price <= upper)
                                         {
                                           double interval = upper - lower;
                                           double time = deadline - datenow;

                                           double score =
                                               (avg_interval / (interval)) +
                                               (time / (avg_time)) +
                                               (amount / (avg_volume));

                                           winners.push_back({id, score, winamount});
                                           total_score += score;
                                         }
                                         else
                                         {
                                           allliqvidation += lossfee;
                                           winamount -= lossfee;

                                           local_txn.exec0("UPDATE bets SET winamount = " + std::to_string(winamount) + " WHERE id = " + std::to_string(id));
                                         }
                                       }
                                       if (total_score == 0.0)
                                       {
                                         for (const auto &bet : bets)
                                         {
                                           int id = bet["id"].as<int>();
                                           double winamount = bet["winamount"].as<double>();
                                           double lossfee = bet["lossfee"].as<double>();
                                           winamount += lossfee;

                                           local_txn.exec0("UPDATE bets SET winamount = " + std::to_string(winamount) + " WHERE id = " + std::to_string(id));
                                         }
                                       }
                                       else
                                       {
                                         for (const auto &winner : winners)
                                         {
                                           double reward_share = winner.score / total_score;
                                           double reward = reward_share * allliqvidation;

                                           local_txn.exec0("UPDATE bets SET winamount = " + std::to_string(winner.winamount + reward) + " WHERE id = " + std::to_string(winner.id));
                                         }
                                       }
                                       local_txn.commit();
                                     }
                                     catch (const std::exception &e)
                                     {
                                       std::cerr << "Error in pararel programing " << e.what() << std::endl;
                                     }
                                   }));
    }

    for (auto &fut : futures)
    {
      fut.get();
    }
  }
  catch (const std::exception &e)
  {
    std::cerr << "Error: " << e.what() << std::endl;
  }
}
