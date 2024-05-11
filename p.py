import streamlit as st
import matplotlib.pyplot as plt

def main():
    st.title('最小二乗法の計算！')
    
    # データの数を入力するテキストボックスを表示
    data_count = st.text_input('データの数を入力してください', value='3')
    st.sidebar.title("グラフの設定")
    xlabel = st.sidebar.text_input("横軸の名称")
    ylabel = st.sidebar.text_input("縦軸の名称")
    showsubmemori = st.sidebar.checkbox("補助目盛りの表示")
    showsubline = st.sidebar.checkbox("補助目盛り線の表示")
    deletemainline = st.sidebar.checkbox("主目盛の目盛り線の非表示")

    # 入力された値が数字かどうかをチェック
    if data_count.isdigit():
        data_count = int(data_count)
        st.write(f'データ数: {data_count}')
        
        # xとyのデータを格納するリスト
        x_data = []
        y_data = []
        
        # 入力欄を表示
        for i in range(data_count):
            # xの入力欄を右に、yの入力欄を左に表示
            col1, col2 = st.columns(2)
            with col1:
                x_input = st.text_input(f'X{i+1}')
            with col2:
                y_input = st.text_input(f'Y{i+1}')
            
            # 入力が空でない場合にのみ浮動小数点数に変換し、リストに追加
            if x_input.isdigit() and x_input.strip() != '':
                x_data.append(float(x_input))
            if y_input.isdigit() and y_input.strip() != '':
                y_data.append(float(y_input))
        
        x_canuse = len(x_data) == data_count and x_data
        y_canuse = len(y_data) == data_count and y_data
        if x_canuse and y_canuse and data_count >= 3:
            # 傾きと切片の計算
            sum_x = sum(x_data)
            sum_y = sum(y_data)
            sum_x_squared = sum(x ** 2 for x in x_data)
            sum_xy = sum(x * y for x, y in zip(x_data, y_data))
            n = len(x_data)

            delta = n * sum_x_squared - sum_x ** 2
            slope = (n * sum_xy - sum_x * sum_y) / delta
            intercept = (sum_x_squared * sum_y - sum_x * sum_xy) / delta

            # 傾きと切片の誤差の計算
            residual = sum((y - slope * x - intercept) ** 2 for x, y in zip(x_data, y_data))
            sigma = (residual / (n - 2)) ** 0.5
            sigma_slope = (n / delta) ** 0.5 * sigma
            sigma_intercept = (sum_x_squared / delta) ** 0.5 * sigma

            # 結果の表示
            st.write("傾き: ", slope)
            st.write("傾きの誤差: ", sigma_slope)
            st.write("切片: ", intercept)
            st.write("切片の誤差: ", sigma_intercept)
            
            # グラフの描画
            start_y = intercept
            end_y = slope * max(x_data) + intercept 
            x_values = [0, max(x_data)]
            y_values = [start_y, end_y]
            fig, ax = plt.subplots()
            plt.plot(x_values, y_values)
            plt.xlim(0,max(x_data))
            plt.ylim(0,max(y_data))  
            plt.xlabel(f'{xlabel}')
            plt.ylabel(f'{ylabel}')
            ax.grid()
            if showsubmemori:
                ax.minorticks_on()
            if deletemainline:
                ax.grid(False)        
            if showsubline:
                ax.grid(which="minor")
            st.pyplot(fig)
        elif data_count < 3:
            st.write("データ数が不足しています。")
        else:
            st.write("データが入力されていません。")
    else:
        st.write('データの数は数字で入力してください。')

if __name__ == "__main__":
    main()