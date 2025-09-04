# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session (Snis does not need this line)
from snowflake.snowpark.functions import col

title = st.text_input('Movie Title', 'Life of Biran')
st.write('Current Movide Title is:',title)
# Write directly to the app
st.title(f"Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie would be:', name_on_order)
# option = st.selectbox('What is your favorite fruit',
# ('Banana', 'Peach', 'Apple'))
# st.write('Your favorite Fruit is: ' , option)

#session = get_active_session()
# my_dataframe=session.table("smoothies.public.fruit_options")
#st.dataframe(data=my_dataframe, use_container_width=True)

session = get_active_session()
my_dataframe=session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=3)

if ingredients_list:
  #st.write(ingredients_list)
  #st.text(ingredients_list)
    
  ingredients_string=''
  for fruit_chose in ingredients_list:
    ingredients_string += fruit_chose + ' '
  st.write(ingredients_string)

  my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """' , '"""+ name_on_order+"""')"""

  st.write(my_insert_stmt)
  #st.stop()
  time_to_insert = st.button('Submit Order')
 # if ingredients_string :
  if time_to_insert : 
      session.sql(my_insert_stmt).collect()
      st.success('Your Smoothie ' + name_on_order + ' is ordered!', icon="✅")
