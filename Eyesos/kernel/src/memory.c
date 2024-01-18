
#include <stdio.h>
#include "memory.h"

void memory_init() {
    printf("Memory: Initializing memory...\n");
    // 初始化內存
}

void memory_allocate(int size) {
    printf("Memory: Allocating %d bytes of memory...\n", size);
    // 分配指定大小的內存
}

void memory_free(void* ptr) {
    printf("Memory: Freeing memory at %p...\n", ptr);
    // 釋放指定地址的內存
}