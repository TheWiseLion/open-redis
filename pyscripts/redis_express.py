from open_redis.deployment import REDIS_PATH, VERSION

def main():
    print("Redis install location: "+REDIS_PATH)
    print("Using Redis Version: "+VERSION)
    

if __name__ == '__main__':
    main()
