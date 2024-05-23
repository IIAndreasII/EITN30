// #ifndef __QUEUE_H__
// #define __QUEUE_H__

// #include <queue>
// #include <mutex>
// #include <condition_variable>


// template<typename T>
// class Queue
// {
// public:
//     Queue() = default;
//     Queue(const Queue&) = delete;
//     Queue(Queue&&) = delete;

//     ~Queue() = default;


// void push(T& item)
// {
//     {
//         std::lock_guard<std::mutex> lock(mut);
//         myQueue.push(item);
//     }
//     cond.notify_one();
// }
    
 
// bool tryPop(T& item)
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


// void waitPop(T& item)
// {
//     std::unique_lock<std::mutex> lock(mut);
//     while (myQueue.empty())
//     {
//         cond.wait(lock);
//     }

//     item = myQueue.front();
//     myQueue.pop();
// }


// bool tryWaitPop(T& item, int millis)
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


// bool empty()
// {
//     std::lock_guard<std::mutex> lock(mut);
//     return myQueue.empty();
// }

// private:
//     std::queue<T> myQueue;
//     mutable std::mutex mut;
//     std::condition_variable cond;
// };

// #endif

#pragma once
#include <queue>
#include <mutex>
#include <condition_variable>

template<typename T>
class Queue {
public:
    void push(T const& _data)
    {
        {
            std::lock_guard<std::mutex> lock(guard);
            queue.push(_data);
        }
        signal.notify_one();
    }

    bool empty() const
    {
        std::lock_guard<std::mutex> lock(guard);
        return queue.empty();
    }

    bool tryPop(T& _value)
    {
        std::lock_guard<std::mutex> lock(guard);
        if (queue.empty())
        {
            return false;
        }

        _value = queue.front();
        queue.pop();
        return true;
    }

    void waitPop(T& _value)
    {
        std::unique_lock<std::mutex> lock(guard);
        while (queue.empty())
        {
            signal.wait(lock);
        }

        _value = queue.front();
        queue.pop();
    }

    bool tryWaitAndPop(T& _value, int _milli)
    {
        std::unique_lock<std::mutex> lock(guard);
        while (queue.empty())
        {
            signal.wait_for(lock, std::chrono::milliseconds(_milli));
            return false;
        }

        _value = queue.front();
        queue.pop();
        return true;
    }

private:
    std::queue<T> queue;
    mutable std::mutex guard;
    std::condition_variable signal;
};