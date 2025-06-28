import streamlit as st
import random

# ------------------- 抽卡參數 -------------------
initial_5star_prob = 0.006
prob_increase_per_draw = 0.06
prob_up = 0.55  # UP角色機率

# ------------------- 抽卡機率邏輯 -------------------
def get_5star_prob(pity):
    if pity < 73:
        return initial_5star_prob
    elif pity < 90:
        return min(1.0, initial_5star_prob + (pity - 73 + 1) * prob_increase_per_draw)
    else:
        return 1.0

def get_4star_prob(pity):
    if pity <= 8:
        return 0.051
    elif pity == 9:
        return 0.562
    else:
        return 1.0

# ------------------- 主模擬函數 -------------------
def simulate_fixed_draws_detailed(total_draws=450):
    pity_5 = 0
    pity_4 = 0
    guaranteed_next_up = False
    up_count = 0
    standard_count = 0
    four_star_count = 0
    stardust = 0
    stardust_draws = 0

    first_5star_obtained = False
    first_4star_obtained = False
    current_draws = 0
    five_star_history = []

    while current_draws < total_draws or stardust >= 5:
        # 星輝兌換抽
        while stardust >= 5 and current_draws < total_draws + 1000:
            stardust -= 5
            stardust_draws += 1
            pity_5 += 1
            pity_4 += 1
            draw_index = current_draws + stardust_draws

            if random.random() < get_5star_prob(pity_5):
                pity_5 = 0
                got_up = False
                if guaranteed_next_up:
                    up_count += 1
                    got_up = True
                    guaranteed_next_up = False
                else:
                    if random.random() < prob_up:
                        up_count += 1
                        got_up = True
                    else:
                        standard_count += 1
                        guaranteed_next_up = True
                five_star_history.append({"draw": draw_index, "type": "UP角色" if got_up else "常駐角色"})
                if first_5star_obtained:
                    stardust += 5
                else:
                    first_5star_obtained = True

            elif random.random() < get_4star_prob(pity_4):
                pity_4 = 0
                four_star_count += 1
                if first_4star_obtained:
                    stardust += 2
                else:
                    first_4star_obtained = True

        # 原始抽
        if current_draws < total_draws:
            current_draws += 1
            pity_5 += 1
            pity_4 += 1
            draw_index = current_draws + stardust_draws

            if random.random() < get_5star_prob(pity_5):
                pity_5 = 0
                got_up = False
                if guaranteed_next_up:
                    up_count += 1
                    got_up = True
                    guaranteed_next_up = False
                else:
                    if random.random() < prob_up:
                        up_count += 1
                        got_up = True
                    else:
                        standard_count += 1
                        guaranteed_next_up = True
                five_star_history.append({"draw": draw_index, "type": "UP角色" if got_up else "常駐角色"})
                if first_5star_obtained:
                    stardust += 5
                else:
                    first_5star_obtained = True

            elif random.random() < get_4star_prob(pity_4):
                pity_4 = 0
                four_star_count += 1
                if first_4star_obtained:
                    stardust += 2
                else:
                    first_4star_obtained = True

    return {
        "UP角色": up_count,
        "常駐角色": standard_count,
        "4星角色": four_star_count,
        "星輝抽數": stardust_draws,
        "總抽數": current_draws + stardust_draws,
        "金色歷史": five_star_history
    }

# ------------------- Streamlit App -------------------
st.title("🌟 抽卡模擬器 - UP vs 常駐")
total_draws = st.number_input("請輸入想抽的總抽數：", min_value=1, max_value=2000, value=450)

if st.button("開始模擬"):
    result = simulate_fixed_draws_detailed(total_draws)

    st.subheader("🎯 模擬結果")
    st.write(f"抽到 UP角色：{result['UP角色']} 次")
    st.write(f"抽到 常駐角色：{result['常駐角色']} 次")
    st.write(f"抽到 4星角色：{result['4星角色']} 次")
    st.write(f"星輝兌換免費抽卡次數：{result['星輝抽數']} 次")
    st.write(f"總抽卡次數（含免費抽）：{result['總抽數']} 次")

    st.subheader("⭐ 出金歷史紀錄")
    for entry in result['金色歷史']:
        st.write(f"第 {entry['draw']} 抽 - {entry['type']}")

    # 記錄歷史結果
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append(result)

if "history" in st.session_state and st.session_state.history:
    st.subheader("📜 歷史模擬記錄")
    for i, record in enumerate(reversed(st.session_state.history[-5:]), 1):
        st.write(f"第 {len(st.session_state.history) - i + 1} 次：UP={record['UP角色']} 常駐={record['常駐角色']} 4星={record['4星角色']}")
