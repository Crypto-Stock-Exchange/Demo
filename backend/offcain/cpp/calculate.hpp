#ifndef CALCULATE_HPP
#define CALCULATE_HPP

void calculate_wins_and_losses();

void fill_stock_data();

std::string read_secret(const std::string &key);

size_t WriteCallback(void *contents, size_t size, size_t nmemb, std::string *output);

#endif
