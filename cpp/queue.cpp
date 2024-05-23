#include "queue.h"


// template<typename T>
// void Queue<T>::push(T& item)
// {
//     {
//         std::lock_guard<std::mutex> lock(mut);
//         myQueue.push(item);
//     }
//     cond.notify_one();
// }
    
// template<typename T>    
// bool Queue<T>::tryPop(T& item)
// {
//     std::lock_guard<std::mutex> lock(mut);
//     if (myQueue.empty())
//     {
//         return false;
//     }

//     item = myQueue.front();
//     myQueue.pop();
//     return true;
// }

// template<typename T>
// void Queue<T>::waitPop(T& item)
// {
//     std::unique_lock<std::mutex> lock(mut);
//     while (myQueue.empty())
//     {
//         cond.wait(lock);
//     }

//     item = myQueue.front();
//     myQueue.pop();
// }

// template<typename T>
// bool Queue<T>::tryWaitPop(T& item, int millis)
// {
//     std::unique_lock<std::mutex> lock(mut);
//     while (myQueue.empty())
//     {
//         cond.wait_for(lock, std::chrono::milliseconds(millis));
//         return false;
//     }

//     item = myQueue.front();
//     myQueue.pop();

//     return true;
// }

// template<typename T>
// bool Queue<T>::empty()
// {
//     std::lock_guard<std::mutex> lock(mut);
//     return myQueue.empty();
// }
