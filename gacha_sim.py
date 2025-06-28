import streamlit as st
import random

# 抽卡機制參數
initial_5star_prob = 0.006
prob_increase_per_draw = 0.06  # 從第74抽起增加
prob_up = 0.55  # 5★中是UP角色的機率

# 計算目前5★機率
def get_5star_prob(pity):
    if pity < 73:
        return initial_5star_prob
    elif pity < 90:
        return min(1.0, initial_5star_prob + (pity - 73 + 1) * prob_increase_per_draw)
    else:
        return 1.0

# 計算目前4★機率
def get_4star_prob(pity):
    if pity <= 8:
        return 0.051
    elif pity == 9:
        return 0.562
    else:
        return 1.0

# 模擬抽卡
def simulate_fixed_draws_detailed(total_draws=450):
    pity_5 = 0
    pity_4 = 0
    guaranteed_next_up = False
    up_count = 0
    standard_count = 0
    four_star_count = 0
    stardust = 0
    stardust_draws = 0

    first_5star = False
    first_4star = False

    current_draws = 0
    five_star_history = []

    while current_draws < total_draws or stardust >= 5:
        # 星輝免費抽
        while stardust >= 5 and current_draws < total_draws + 1000:
            stardust -= 5
            stardust_draws += 1
            pity_5 += 1
            pity_4 += 1

            if random.random() < get_5star_prob(pity_5):
                draw_num = current_draws + stardust_draws
                pity_5_counter = pity_5
                pity_5 = 0
                got_up = False

                if guaranteed_next_up:
                    up_count += 1
                    guaranteed_next_up = False
                    got_up = True
                else:
                    if random.random() < prob_up:
                        up_count += 1
                        got_up = True
                    else:
                        standard_count += 1
                        guaranteed_next_up = True

                if first_5star:
                    stardust += 5
                else:
                    first_5star = True

                five_star_history.append({
                    "draw": draw_num,
                    "type": "UP角色" if got_up else "常駐角色",
                    "pity": pity_5_counter
                })

            elif random.random() < get_4star_prob(pity_4):
                pity_4 = 0
                four_star_count += 1
                if first_4star:
                    stardust += 2
                else:
                    first_4star = True

        # 原始抽
        if current_draws < total_draws:
            current_draws += 1
            pity_5 += 1
            pity_4 += 1

            if random.random() < get_5star_prob(pity_5):
                draw_num = current_draws + stardust_draws
                pity_5_counter = pity_5
                pity_5 = 0
                got_up = False

                if guaranteed_next_up:
                    up_count += 1
                    guaranteed_next_up = False
                    got_up = True
                else:
                    if random.random() < prob_up:
                        up_count += 1
                        got_up = True
                    else:
                        standard_count += 1
                        guaranteed_next_up = True

                if first_5star:
                    stardust += 5
                else:
                    first_5star = True

                five_star_history.append({
                    "draw": draw_num,
                    "type": "UP角色" if got_up else "常駐角色",
                    "pity": pity_5_counter
                })

            elif random.random() < get_4star_prob(pity_4):
                pity_4 = 0
                four_star_count += 1
                if first_4star:
                    stardust += 2
                else:
                    first_4star = True

    return {
        "UP角色": up_count,
        "常駐角色": standard_count,
        "4star": four_star_count,
        "extra_draws_from_stardust": stardust_draws,
        "total_draws_used": current_draws + stardust_draws,
        "five_star_history": five_star_history
    }

# Streamlit UI
st.title("🎯 抽卡模擬器")

if "history" not in st.session_state:
    st.session_state["history"] = []

user_input = st.number_input("請輸入你想抽的次數：", min_value=1, max_value=3000, value=450)

if st.button("開始模擬！"):
    result = simulate_fixed_draws_detailed(user_input)
    st.session_state["history"].append(result)

    st.subheader("✨ 模擬結果 ✨")
    st.write(f"抽到 UP角色：{result['UP角色']} 次")
    st.write(f"抽到 常駐角色：{result['常駐角色']} 次")
    st.write(f"抽到 4★：{result['4star']} 次")
    st.write(f"星輝免費抽：{result['extra_draws_from_stardust']} 次")
    st.write(f"總抽數（含免費）：{result['total_draws_used']} 次")

    st.subheader("📌 每次出金紀錄")
    for item in result["five_star_history"]:
        st.write(f"第 {item['draw']} 抽 - {item['type']}（距上次5★ {item['pity']} 抽）")

st.subheader("📜 過往模擬記錄")
if st.checkbox("顯示最近 5 次模擬紀錄"):
    for i, record in enumerate(reversed(st.session_state["history"][-5:]), 1):
        up = record.get("UP角色", record.get("A", 0))
        standard = record.get("常駐角色", record.get("B", 0))
        four_star = record.get("4star", 0)
        extra_draws = record.get("extra_draws_from_stardust", 0)
        total_used = record.get("total_draws_used", "?")
        five_star_draws = record.get("five_star_history", [])

        with st.expander(f"第 {-i} 次模擬：共 {total_used} 抽（UP={up} 常駐={standard} 4★={four_star}）"):
            st.write(f"星輝免費抽次數：{extra_draws}")
            st.write("出金紀錄：")
            for item in five_star_draws:
                st.write(f"🎯 第 {item['draw']} 抽 - {item['type']}（距上次5★ {item['pity']} 抽）")

