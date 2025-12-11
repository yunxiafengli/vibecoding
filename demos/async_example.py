import asyncio
import aiohttp
import time

# async/await基本概念示例
async def fetch_data(url):
    """异步获取数据"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    # 并发执行多个异步任务
    urls = [
        'https://httpbin.org/delay/1',
        'https://httpbin.org/delay/2',
        'https://httpbin.org/delay/3'
    ]
    
    # 使用asyncio.gather并发执行
    start_time = time.time()
    results = await asyncio.gather(
        *[fetch_data(url) for url in urls]
    )
    end_time = time.time()
    
    print(f"并发执行时间: {end_time - start_time:.2f}秒")
    print(f"获取到 {len(results)} 个结果")

# 异步上下文管理器示例
class AsyncDatabase:
    async def __aenter__(self):
        await asyncio.sleep(0.1)  # 模拟连接数据库
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await asyncio.sleep(0.1)  # 模拟关闭连接
    
    async def query(self, sql):
        await asyncio.sleep(0.5)  # 模拟查询
        return f"Query result for: {sql}"

async def database_example():
    async with AsyncDatabase() as db:
        result = await db.query("SELECT * FROM users")
        return result

# 常见陷阱示例
async def common_pitfalls():
    # 陷阱1: 阻塞操作
    # time.sleep(3)  # 这会阻塞整个事件循环！
    await asyncio.sleep(3)  # 正确做法
    
    # 陷阱2: 忘记await
    # task = asyncio.create_task(some_async_func())  # 创建任务但不等待
    # result = await task  # 正确做法
    
    # 陷阱3: 异常处理
    try:
        await asyncio.sleep(1)
        raise ValueError("示例错误")
    except ValueError as e:
        print(f"捕获异常: {e}")

if __name__ == "__main__":
    # 运行异步程序
    asyncio.run(main())