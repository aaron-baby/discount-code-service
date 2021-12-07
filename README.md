# discount-code-service
[Design](./design.md)
## 1. Application setup
```shell
# Create a virtual environment to isolate our package dependencies locally
python3 -m venv venv
source venv/bin/activate  # On Windows use `env\Scripts\activate`

pip install --requirement requirements.txt
```

## 2. Start a local redis instance
```shell
docker run --name discount-code-redis --rm -p6379:6379 -d redis
```

## 3. Run Flask Application
```shell
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
or run on an alternative port `5001`

    flask run --port 5001

## 4. Validate the endpoints
### i) generate discount codes
    curl http://127.0.0.1:5000/generate_codes\?brand_id\=1\&codes_number\=10
While everything goes right, got below response
```shell
{
  "generated_codes_number": 10
}
```
Then open Redis client should see similar results
```shell
~ redis-cli
127.0.0.1:6379> smembers brand:1
 1) "a074d1bb-128c-43ee-9b70-02ea5e894d78"
 2) "bd13006e-8cad-40b2-872e-445fe8003a0b"
 3) "768f7b11-dfe2-40ef-a21f-69fa5ef51c80"
 4) "9f26101c-b2e1-47f3-a2f6-b307532c26df"
 5) "2400ff6b-653e-40d9-aae3-5d4fe7b86508"
 6) "f3b4c684-cb1e-471f-8a20-24253df32987"
 7) "63a6f63d-9ea9-4391-9a73-145b59290422"
 8) "73f56230-be0a-468a-adcc-1b253441d9b7"
 9) "c8183415-0dce-46f5-b604-13dec99830f7"
10) "54b654a4-d274-4e70-9d8e-c344da8f477a"
```
### ii) get a discount code
```shell
~ curl http://127.0.0.1:5000/get_code\?user_id\=1\&brand_id\=1
{
  "code": "768f7b11-dfe2-40ef-a21f-69fa5ef51c80"
}
```
then one of the generated code should be moved out from `brand:{id}` to `brand:{id}_assigned`
```shell
127.0.0.1:6379> smembers brand:1_assigned
1) "768f7b11-dfe2-40ef-a21f-69fa5ef51c80"
```