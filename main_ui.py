import streamlit as st
from supabase import create_client,client
from purchase import buy_coin

supabase_url ="https://ctbpovmhgakrageabszx.supabase.co"
supabase_key ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN0YnBvdm1oZ2FrcmFnZWFic3p4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTExODM0OTksImV4cCI6MjA2Njc1OTQ5OX0.5m2mHTmV3rh8xPSPctGl20h1zSna8ZYd3wgplxMuMI0"
client = create_client(supabase_url,supabase_key)

if "page" not in st.session_state:
    st.session_state.page = "landing"

if st.session_state.page == "landing":
    st.title("Welcome to CryptoHub")
    st.subheader("Know, Track & Trade your favorite Crypto coins!")
    st.write("This platform helps you view, wishlist, buy and exchange the top 30 cryptocurrencies.")
    if st.button("Get Started",type="primary",use_container_width=False):

        st.session_state.page = "auth"

elif st.session_state.page == "auth":
    tab1, tab2 = st.tabs([" Login", "Register"])

    with tab1:
        st.subheader("Login to your account")
        login_userid = st.text_input("User ID",key="login_userid_mainui",placeholder="Enter your User Id")
        login_password = st.text_input("Password",key="login_password_mainui",placeholder="Enter your Password",type="password")

        if st.button("Login",type="primary",use_container_width=False):
            response = client.table("users").select("*").eq("userid", login_userid).eq("password", login_password).execute()
            if response.data:
                st.success("Login successfull!")
                st.balloons()
                st.session_state.user_id = login_userid
                current_balance = float(response.data[0]["balance"])
                new_balance = current_balance + 5000000
                client.table("users").update({"balance": new_balance}).eq("userid", login_userid).execute()

                st.session_state.page = "home"  
            else:
                st.error("Invalid credentials. Please register.")

    with tab2:
        st.subheader("Create a new account")
        first_name = st.text_input("First Name",placeholder="Enter your First Name")
        last_name = st.text_input("Last Name",placeholder="Enter your Last Name")
        register_userid = st.text_input("User ID",key="register_userid_mainui",placeholder="Enter User Id")
        register_password = st.text_input("Password",key="register_password_mainui",placeholder="Set a Password",type="password")

        if st.button("Register",type="primary",use_container_width=False):
        
            existing = client.table("users").select("*").eq("userid", register_userid).execute()
            if existing.data:
                st.warning(" User ID already exists. Try logging in.")
            else:
                client.table("users").insert({
                    "first_name": first_name,
                    "last_name": last_name,
                    "userid": register_userid,
                    "password": register_password,
                    "balance": 0
                }).execute()
                st.success("Successfully registered! You can now login.")
elif st.session_state.page == "home":
    if "show_wishlist" not in st.session_state:
        st.session_state.show_wishlist = False

    coin_response = coin_response = client.table("coins").select("*").order("coinid", desc=False).execute()
    coins = coin_response.data

    wishlist = client.table("wishlist").select("coinid,coin_name,coin_price").eq("userid", st.session_state.user_id).execute().data or []

    st.title(f"Welcome, {st.session_state.user_id}!")
    st.badge("As Welcome Bonus we added Rs.5,000,000 to your current wallet")

    main_col, wishlist_col = st.columns([200,120], gap="large")
    with wishlist_col:
        if st.button("View Wishlist",type="primary",use_container_width=False):
           st.badge("Click here to check balance and wishlist")
           st.session_state.show_wishlist = not st.session_state.show_wishlist
        if st.session_state.show_wishlist:
          st.markdown("Your Wishlist")
          header1, header2, header3 = st.columns([10,11.5,10])
          header1.markdown("**Coin ID**")
          header2.markdown("**Coin Name**")
          header3.markdown("**Coin Price**")
          for item in wishlist:
             col1, col2, col3 = st.columns([10,11.5,10])
             col1.markdown(f"{item['coinid']}")
             col2.markdown(f"{item['coin_name']}")
             col3.markdown(f"{item['coin_price']}")
          st.markdown("---")

          balance = client.table("users").select("balance").eq("userid", st.session_state.user_id).execute().data[0]["balance"]
          st.markdown("your Wallet")
          st.markdown(f"Current Balance: Rs.{balance}")

          purchases = client.table("purchases").select("coinid","coin_name", "coin_price","action_type").eq("userid", st.session_state.user_id).execute().data or []
          if purchases:
              st.markdown("Your Purchased Coins")
              h1,h2, h3,h4 = st.columns([10,11,10.5,9])
              h1.markdown("Coin Id")
              h2.markdown("Coin Name")
              h3.markdown("Coin Price")
              h4.markdown("Type")
        
              for item in purchases:
                  col1, col2, col3,col4 = st.columns([10,11,10.5,9])
                  col1.markdown(f"{item["coinid"]}")
                  col2.markdown(f"{item["coin_name"]}")
                  col3.markdown(f"{item["coin_price"]}")
                  col4.markdown(f"{item['action_type']}")
    with main_col: 
     if coins:
        header1, header2, header3, _, _,_ = st.columns([32,32,32,32,36,36])
        header1.markdown("**Coin ID**")
        header2.markdown("**Coin Name**")
        header3.markdown("**Coin Price**")

     for coin in coins:
        with st.container():
            col1, col2, col3, col4,col5,col6 = st.columns([32,32,32,32,36,36])
            col1.markdown(f"**{coin['coinid']}**")
            col2.markdown(f"**{coin['coin_name']}**")
            col3.markdown(f"Rs.{coin['coin_price']}")
            coin_key = coin["coin_name"]

            if col4.button("WL", key=f"wish_{coin_key}", type="primary",use_container_width=False):
                client.table("wishlist").insert({
                    "userid": st.session_state.user_id,
                    "coinid": coin["coinid"],
                    "coin_name": coin["coin_name"],
                    "coin_price": coin["coin_price"]
                }).execute()
            if col5.button("Buy", key=f"buy_{coin_key}", type="primary",use_container_width=False):
                st.session_state[f"show_payment_{coin_key}"] = True
            if st.session_state.get(f"show_payment_{coin_key}", False):
                st.markdown("Select Payment Method:")
                payment_method = st.radio(
                    "Choose one:",
                    ["Use Wallet Balance", "Use Bank/Card"],
                    key=f"method_{coin_key}"
                )   
                if payment_method == "Use Wallet Balance":
                    if st.button("Confirm Wallet Purchase", key=f"confirm_wallet_{coin_key}"):
                        success, msg = buy_coin(
                            user_id=st.session_state.user_id,
                            coin_id=coin["coinid"],
                            coin_name=coin["coin_name"],
                            coin_price=coin["coin_price"],
                            client=client
                        )
                        if success:
                            st.success(msg)
                            st.session_state[f"show_payment_{coin_key}"] = False
                        else:
                            st.warning(msg)
                elif payment_method == "Use Bank/Card":
                    with st.form(f"bank_form_{coin_key}"):
                        card_number = st.text_input("Card Number", max_chars=16)
                        expiry_date = st.text_input("Expiry Date (MM/YY)", max_chars=5)
                        confirm = st.form_submit_button("Confirm Bank Purchase")
                        if confirm:
                            if card_number and expiry_date:
                                st.warning("Bank payment is not implemented. Please use wallet.")
                            else:
                                st.error("Please fill in all bank details.")
            
            if col6.button("Exc", key=f"exchange_{coin_key}", type="primary",use_container_width=False):
                st.session_state[f"show_exchange_{coin_key}"] = True

            if st.session_state.get(f"show_exchange_{coin_key}", False):
                st.markdown("Exchange Coins")

                user_purchases = client.table("purchases").select("coinid, coin_name, coin_price").eq("userid", st.session_state.user_id).eq("action_type", "purchase").execute().data

                if not user_purchases:
                 st.info("You haven't purchased any coins to exchange.")
                else:
                    purchased_coin_names = [p["coin_name"] for p in user_purchases]
                    target_coin_names = [c["coin_name"] for c in coins if c["coin_name"] not in purchased_coin_names]

                    coin_from = st.selectbox("Select coin to exchange:", purchased_coin_names, key=f"from_{coin_key}")
                    coin_to = st.selectbox("Select coin you want:", target_coin_names, key=f"to_{coin_key}")

                    if st.button("Confirm Exchange", key=f"confirm_exchange_{coin_key}"):
                        from_coin = next((p for p in user_purchases if p["coin_name"] == coin_from), None)
                        to_coin = next((c for c in coins if c["coin_name"] == coin_to), None)

                        if from_coin and to_coin:
                            from_price = float(str(from_coin["coin_price"]).replace("Rs.", "").replace(",", "").strip())
                            to_price = float(str(to_coin["coin_price"]).replace("Rs.", "").replace(",", "").strip())
 

                            if from_price >= to_price:
                                refund = from_price - to_price
                                user_data = client.table("users").select("balance").eq("userid", st.session_state.user_id).execute().data
                                current_balance = float(user_data[0]["balance"])
                                new_balance = current_balance + refund
                                client.table("users").update({"balance": new_balance}).eq("userid", st.session_state.user_id).execute()
                                
                                client.table("users").update({
                                    "exchanged_coins": to_coin["coin_name"],
                                    "exchanged_coin_price": to_coin["coin_price"]
                                }).eq("userid", st.session_state.user_id).execute()

                                client.table("purchases").insert({
                                    "userid": st.session_state.user_id,
                                    "coinid": to_coin["coinid"],
                                    "coin_name": to_coin["coin_name"],
                                    "coin_price": to_coin["coin_price"],
                                    "action_type": "exchange"
                                }).execute()
                                # Delete the original coin that was exchanged
                                client.table("purchases").delete() \
                                    .eq("userid", st.session_state.user_id) \
                                    .eq("coinid", from_coin["coinid"]) \
                                    .eq("action_type", "purchase") \
                                    .execute()



                                st.success(f"Exchanged {coin_from} for {coin_to}. Refund of ${refund:,.2f} added to balance.")
                                st.session_state[f"show_exchange_{coin_key}"] = False
                            else:
                                st.error("Target coin is more expensive. Exchange not allowed.")

