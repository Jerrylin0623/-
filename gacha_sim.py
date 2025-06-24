import streamlit as st
import random

initial_5star_prob = 0.006
prob_increase_per_draw = 0.06
prob_A = 0.55

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

def simulate_fixed_draws_detailed(total_draws=450):
    pity_5 = 0
    pity_4 = 0
    guaranteed_next_A = False
    a_count = 0
    b_count = 0
    four_star_count = 0
    stardust = 0
    stardust_draws = 0
    first_5star_obtained = False
    first_4star_obtained = False
    current_draws = 0

    while current_draws < total_draws or stardust >= 5:
        while stardust >= 5 and current_draws < total_draws + 1000:
            stardust -= 5
            stardust_draws += 1
            pity_5 += 1
            pity_4 += 1

            if random.random() < get_5star_prob(pity_5):
                pity_5 = 0
                if guaranteed_next_A:
                    a_count += 1
                    guaranteed_next_A = False
                else:
                    if random.random() < prob_A:
                        a_count += 1
                    else:
                        b_count += 1
                        guaranteed_next_A = True

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

        if current_draws < total_draws:
            current_draws += 1
            pity_5 += 1
            pity_4 += 1

            if random.random() < get_5star_prob(pity_5):
                pity_5 = 0
                if guaranteed_next_A:
                    a_count += 1
                    guaranteed_next_A = False
                else:
                    if random.random() < prob_A:
                        a_count += 1
                    else:
                        b_count += 1
                        guaranteed_next_A = True

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
        "A": a_count,
        "B": b_count,
        "4star": four_star_count,
        "extra_draws_from_stardust": stardust_draws,
        "total_draws_used": current_draws + stardust_draws
    }

# Streamlit 主程式
st.title("抽卡模擬器（含星輝）")

draws = st.number_input("請輸入你想抽的次數", min_value=1, max_value=10000, value=180)

if st.button("開始模擬！"):
    result = simulate_fixed_draws_detailed(draws)
    st.success(f"模擬完成！你在 {draws} 抽中獲得：")
    st.write(f"⭐ 抽到 A 的數量：{result['A']}")
    st.write(f"⭐ 抽到 B 的數量：{result['B']}")
    st.write(f"✨ 抽到 4★ 的數量：{result['4star']}")
    st.write(f"💎 星輝免費抽卡次數：{result['extra_draws_from_stardust']}")
    st.write(f"🎯 總抽卡次數（含星輝）：{result['total_draws_used']}")
