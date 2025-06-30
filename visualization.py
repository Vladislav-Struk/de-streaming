"""Import libraries."""
import altair as alt
import pandas as pd
import streamlit as st


def main():
    """Visualization of data."""
    types = []
    max_values_of_avg_price = []
    max_values_of_living_area = []
    values_of_summ_advert_count = []
    max_values_price_per_sq = []
    data = pd.read_csv('portugal_listings_out.csv')
    df_avg_price = data.groupby('Type')['avg_price'].agg('max')
    df_avg_living_area = data.groupby('Type')['avg_living_area'].agg('max')
    df_advert_count = data.groupby('Type')['advertisement_count'].agg('sum')
    df_avg_price_sq = data.groupby('Type')['avg_price_per_square'].agg('max')
    for i in range(0, len(data)):
        types.append(data['Type'].iloc[i])
    for i in range(0, len(df_avg_price)):
        max_values_of_avg_price.append(df_avg_price[i])
    for i in range(0, len(df_avg_living_area)):
        max_values_of_living_area.append(df_avg_living_area[i])
    for i in range(0, len(df_advert_count)):
        values_of_summ_advert_count.append(df_advert_count[i])
    for i in range(0, len(df_advert_count)):
        max_values_price_per_sq.append(df_avg_price_sq[i])
    types = list(set(types))
    max_avg_price = {'Property_types': types,
                     'Max_avg_price': max_values_of_avg_price}
    frame_for_max_price = pd.DataFrame(max_avg_price)
    chart_avg_price = alt.Chart(frame_for_max_price).mark_bar()
    chart_avg_price = chart_avg_price.encode(y='Max_avg_price',
                                             x='Property_types')
    chart_avg_price = chart_avg_price.properties(width=600)
    chart_avg_price = chart_avg_price.configure_mark(color='blue')
    st.altair_chart(chart_avg_price)
    max_avg_area = {'Property_types': types,
                    'Max_avg_living_area': max_values_of_living_area}
    frame_for_max_avg_area = pd.DataFrame(max_avg_area)
    chart_avg_area = alt.Chart(frame_for_max_avg_area).mark_bar()
    chart_avg_area = chart_avg_area.encode(y='Max_avg_living_area',
                                           x='Property_types',
                                           color='Property_types')
    st.altair_chart(chart_avg_area,
                    use_container_width=True)
    sum_adv_cnt = {'Property_types': types,
                   'Sum_advirtisements_count': values_of_summ_advert_count}
    frame_for_sum_adv_cnt = pd.DataFrame(sum_adv_cnt)
    chart_adv_sum = alt.Chart(frame_for_sum_adv_cnt).mark_bar()
    chart_adv_sum = chart_adv_sum.encode(y='Sum_advirtisements_count',
                                         x='Property_types')
    chart_adv_sum = chart_adv_sum.properties(width=600)
    chart_adv_sum = chart_adv_sum.configure_mark(color='red')
    st.altair_chart(chart_adv_sum,
                    use_container_width=True)
    max_avg_price_per_sq = {'Property_types': types,
                            'Max_price_per_sq': max_values_price_per_sq}
    frame_for_max_price_per_sq = pd.DataFrame(max_avg_price_per_sq)
    chart_price_per_sq = alt.Chart(frame_for_max_price_per_sq).mark_bar()
    chart_price_per_sq = chart_price_per_sq.encode(y='Max_price_per_sq',
                                                   x='Property_types')
    chart_price_per_sq = chart_price_per_sq.properties(width=600)
    chart_price_per_sq = chart_price_per_sq.configure_mark(color='green')
    st.altair_chart(chart_price_per_sq,
                    use_container_width=True)


if __name__ == '__main__':
    main()
