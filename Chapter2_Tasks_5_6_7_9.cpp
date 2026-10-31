#include <algorithm>
#include <cassert>
#include <cstddef>
#include <iostream>
#include <limits>
#include <list>
#include <stack>
#include <stdexcept>
#include <utility>
#include <vector>

using namespace std;

struct Node {
    int value;
    Node* next = nullptr;
};

// Time: O(n), where n is the number of distinct reachable nodes; extra space: O(1).
bool has_cycle(const Node* head) {
    const Node* slow = head;
    const Node* fast = head;

    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;

        if (slow == fast) {
            return true;
        }
    }

    return false;
}

void test_challenge_5() {
    assert(!has_cycle(nullptr));

    Node single{10};
    assert(!has_cycle(&single));

    single.next = &single;
    assert(has_cycle(&single));

    Node a{7}, b{7}, c{7};
    a.next = &b;
    b.next = &c;
    assert(!has_cycle(&a));

    c.next = &a;
    assert(has_cycle(&a));

    Node n1{1}, n2{2}, n3{3}, n4{4}, n5{5};
    n1.next = &n2;
    n2.next = &n3;
    n3.next = &n4;
    n4.next = &n5;
    n5.next = &n2;
    assert(has_cycle(&n1));

    cout << "Challenge 5: all 6 test cases passed.\n";
}

// Time: O(1) worst case per push/pop/top/get_min; space: O(n), including auxiliary storage.
class MinStack {
private:
    stack<int, list<int>> values_;
    stack<int, list<int>> minimums_;

public:
    void push(int value) {
        const int minimum = minimums_.empty()
                                ? value
                                : min(value, minimums_.top());
        values_.push(value);
        try {
            minimums_.push(minimum);
        } catch (...) {
            values_.pop();
            throw;
        }
    }

    void pop() {
        if (empty()) {
            throw underflow_error("pop() on an empty MinStack");
        }
        values_.pop();
        minimums_.pop();
    }

    int top() const {
        if (empty()) {
            throw underflow_error("top() on an empty MinStack");
        }
        return values_.top();
    }

    int get_min() const {
        if (empty()) {
            throw underflow_error("get_min() on an empty MinStack");
        }
        return minimums_.top();
    }

    bool empty() const {
        return values_.empty();
    }
};

template <typename Action>
void expect_underflow(Action action) {
    bool caught = false;
    try {
        action();
    } catch (const underflow_error&) {
        caught = true;
    }
    assert(caught);
}

void test_challenge_6() {
    MinStack example;
    example.push(3);
    example.push(5);
    example.push(2);
    assert(example.top() == 2 && example.get_min() == 2);
    example.pop();
    assert(example.top() == 5 && example.get_min() == 3);

    MinStack duplicates;
    duplicates.push(2);
    duplicates.push(1);
    duplicates.push(1);
    duplicates.pop();
    assert(duplicates.get_min() == 1);
    duplicates.pop();
    assert(duplicates.get_min() == 2);

    MinStack negatives;
    negatives.push(0);
    negatives.push(-3);
    negatives.push(7);
    assert(negatives.top() == 7 && negatives.get_min() == -3);
    negatives.pop();
    assert(negatives.get_min() == -3);
    negatives.pop();
    assert(negatives.get_min() == 0);

    MinStack reusable;
    reusable.push(42);
    reusable.pop();
    assert(reusable.empty());
    reusable.push(-7);
    assert(reusable.top() == -7 && reusable.get_min() == -7);
    reusable.pop();
    assert(reusable.empty());

    MinStack empty;
    expect_underflow([&] { empty.pop(); });
    expect_underflow([&] { (void)empty.top(); });
    expect_underflow([&] { (void)empty.get_min(); });

    MinStack extremes;
    extremes.push(numeric_limits<int>::max());
    extremes.push(numeric_limits<int>::min());
    assert(extremes.get_min() == numeric_limits<int>::min());
    extremes.pop();
    assert(extremes.get_min() == numeric_limits<int>::max());

    cout << "Challenge 6: all 6 test cases passed.\n";
}

// Time: append O(1) amortized/O(n) on growth, get/set O(1); storage: O(n + 1).
class DynamicArray {
private:
    int* data_;
    size_t size_;
    size_t capacity_;

    void check_index(ptrdiff_t index) const {
        if (index < 0 || static_cast<size_t>(index) >= size_) {
            throw out_of_range("DynamicArray index out of range");
        }
    }

    void grow() {
        if (capacity_ > numeric_limits<size_t>::max() / 2) {
            throw length_error("DynamicArray capacity cannot be doubled");
        }

        const size_t new_capacity = capacity_ * 2;
        int* new_data = new int[new_capacity];
        for (size_t i = 0; i < size_; ++i) {
            new_data[i] = data_[i];
        }

        delete[] data_;
        data_ = new_data;
        capacity_ = new_capacity;
    }

public:
    DynamicArray() : data_(new int[2]), size_(0), capacity_(2) {}

    ~DynamicArray() {
        delete[] data_;
    }

    DynamicArray(const DynamicArray&) = delete;
    DynamicArray& operator=(const DynamicArray&) = delete;

    void append(int value) {
        if (size_ == capacity_) {
            grow();
        }
        data_[size_] = value;
        ++size_;
    }

    int get(ptrdiff_t index) const {
        check_index(index);
        return data_[static_cast<size_t>(index)];
    }

    void set(ptrdiff_t index, int value) {
        check_index(index);
        data_[static_cast<size_t>(index)] = value;
    }

    size_t size() const { return size_; }
    size_t capacity() const { return capacity_; }
};

template <typename Action>
void expect_out_of_range(Action action) {
    bool caught = false;
    try {
        action();
    } catch (const out_of_range&) {
        caught = true;
    }
    assert(caught);
}

void test_challenge_7() {
    DynamicArray array;
    assert(array.size() == 0 && array.capacity() == 2);
    expect_out_of_range([&] { (void)array.get(0); });
    expect_out_of_range([&] { array.set(0, 99); });

    array.append(10);
    array.append(20);
    assert(array.size() == 2 && array.capacity() == 2);
    assert(array.get(0) == 10 && array.get(1) == 20);

    array.append(30);
    assert(array.size() == 3 && array.capacity() == 4);
    assert(array.get(0) == 10 && array.get(1) == 20 && array.get(2) == 30);

    array.set(0, -10);
    array.set(2, 0);
    assert(array.get(0) == -10 && array.get(1) == 20 && array.get(2) == 0);
    assert(array.size() == 3 && array.capacity() == 4);

    expect_out_of_range([&] { (void)array.get(-1); });
    expect_out_of_range([&] { array.set(-1, 99); });
    expect_out_of_range([&] { (void)array.get(3); });
    expect_out_of_range([&] { array.set(3, 99); });
    expect_out_of_range([&] { (void)array.get(100); });
    expect_out_of_range([&] { array.set(100, 99); });

    DynamicArray many;
    for (int i = 0; i < 1000; ++i) {
        many.append(i - 500);
    }
    assert(many.size() == 1000 && many.capacity() == 1024);
    for (int i = 0; i < 1000; ++i) {
        assert(many.get(i) == i - 500);
    }
    many.set(999, 12345);
    assert(many.get(999) == 12345);

    cout << "Challenge 7: all 6 test cases passed.\n";
}

using IndexRange = pair<ptrdiff_t, ptrdiff_t>;

// Time: O(log n); extra space: O(1).
IndexRange search_range(const vector<int>& nums, int target) {
    size_t left = 0;
    size_t right = nums.size();

    while (left < right) {
        const size_t middle = left + (right - left) / 2;
        if (nums[middle] < target) {
            left = middle + 1;
        } else {
            right = middle;
        }
    }

    const size_t first = left;
    if (first == nums.size() || nums[first] != target) {
        return {-1, -1};
    }

    left = first;
    right = nums.size();
    while (left < right) {
        const size_t middle = left + (right - left) / 2;
        if (nums[middle] <= target) {
            left = middle + 1;
        } else {
            right = middle;
        }
    }

    return {static_cast<ptrdiff_t>(first),
            static_cast<ptrdiff_t>(left - 1)};
}

void test_challenge_9() {
    const vector<int> example{5, 7, 7, 8, 8, 8, 10};
    assert((search_range(example, 8) == IndexRange{3, 5}));

    assert((search_range(example, 6) == IndexRange{-1, -1}));
    assert((search_range(example, 0) == IndexRange{-1, -1}));
    assert((search_range(example, 11) == IndexRange{-1, -1}));

    assert((search_range(example, 10) == IndexRange{6, 6}));

    assert((search_range({}, 8) == IndexRange{-1, -1}));

    assert((search_range({4}, 4) == IndexRange{0, 0}));
    assert((search_range({4}, 5) == IndexRange{-1, -1}));

    assert((search_range({2, 2, 2, 2}, 2) == IndexRange{0, 3}));

    assert((search_range({1, 1, 2, 3}, 1) == IndexRange{0, 1}));
    assert((search_range({1, 2, 3, 3}, 3) == IndexRange{2, 3}));

    assert((search_range({-5, -2, -2, 0}, -2) == IndexRange{1, 2}));

    const int low = numeric_limits<int>::min();
    const int high = numeric_limits<int>::max();
    const vector<int> extremes{low, low, 0, high, high};
    assert((search_range(extremes, low) == IndexRange{0, 1}));
    assert((search_range(extremes, high) == IndexRange{3, 4}));

    cout << "Challenge 9: all 9 test cases passed.\n";
}

int main() {
    test_challenge_5();
    test_challenge_6();
    test_challenge_7();
    test_challenge_9();
    return 0;
}
