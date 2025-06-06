#include <iostream>
#include <thread>
#include <chrono>
#include <atomic>
#include <csignal>

#include "calculate.hpp"

std::atomic<bool> keepRunning(true);

void signal_handler(int signal)
{
  keepRunning = false;
}

int main()
{

  std::signal(SIGINT, signal_handler);

  while (keepRunning)
  {
    auto start = std::chrono::steady_clock::now();

    fill_stock_data();

    calculate_wins_and_losses();

    auto end = std::chrono::steady_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::this_thread::sleep_for(std::chrono::seconds(60) - elapsed);
  }

  std::cout << "Program Stoped" << std::endl;
  return 0;
}
