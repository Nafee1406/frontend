from datetime import datetime

def buy_coin(user_id, coin_id, coin_name, coin_price, client):
    coin_price = float(str(coin_price).replace("Rs.", "").replace(",", "").strip())
    user_data = client.table("users").select("balance").eq("userid", user_id).execute().data
    if not user_data:
        return False, "User not found."

    current_balance = float(user_data[0]['balance'])
    if current_balance >=coin_price:
         new_balance = current_balance - coin_price
         client.table("users").update({"balance": new_balance}).eq("userid", user_id).execute()
         client.table("purchases").insert({
                "userid": user_id,
                "coinid": coin_id,
                "coin_name": coin_name,
                "coin_price": float(coin_price),
                "action_type": "purchase"
            }).execute()

         client.table("users").update({"balance": new_balance}).eq("userid", user_id).execute()
         return True, f"You purchased 1 {coin_name} for Rs.{coin_price}"
    else:
        return False, "Insufficient balance to complete this purchase."
    