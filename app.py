import streamlit as st
from copy import deepcopy
import random


st.set_page_config(
    page_title='Multiple pages',
    layout="wide"
)

income_constant_mapping = {
    '爱迪生': 1.75,
    '特斯拉': 1,
    '慈禧': 0.5,
    '尼古拉斯二世': 1,
    '袁隆平': 1,
    '成吉思汗': 1,
    '秦始皇': 1,
    '明治天皇': 1.1,
    '罗斯福': 1.35,
    '刘秀': 1,
    '奥本海默': 1,
    '腓特烈二世': 1
}

build_constant_mapping = {
    '爱迪生': 1,
    '特斯拉': 1,
    '慈禧': 0.9,
    '尼古拉斯二世': 1,
    '袁隆平': 1,
    '成吉思汗': 1,
    '秦始皇': 0.5,
    '明治天皇': 1,
    '罗斯福': 1,
    '刘秀': 1,
    '奥本海默': 1,
    '腓特烈二世': 1
}

soldier_constant_mapping = {
    '爱迪生': 1,
    '特斯拉': 1,
    '慈禧': 1,
    '尼古拉斯二世': 1,
    '袁隆平': 1,
    '成吉思汗': 1,
    '秦始皇': 0.5,
    '明治天皇': 1,
    '罗斯福': 1,
    '刘秀': 1,
    '奥本海默': 1,
    '腓特烈二世': 1
}



col1, col2, col3, col4, col5 = st.columns(5)

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    
if 'char_idx_tuple' not in st.session_state:
    st.session_state.char_idx_tuple = (0, 0, 0, 0)

num_players = 4
def initialize_player_files(num_players):
    player_resource = dict()
    add_resource = dict()
    for i in range(1, num_players+1):
        res = {'money':1000}
        player_resource[i] = res
        add_resource[i] = dict()
    
    return player_resource, add_resource

if 'player_resource_dict' not in st.session_state:
    player_resource_dict, player_addresource_dict = initialize_player_files(num_players)
    st.session_state.player_resource_dict = player_resource_dict
    st.session_state.player_addresource_dict = player_addresource_dict

if 'piece_killed_dict' not in st.session_state:
    st.session_state.piece_killed_dict = dict()
    
if 'player_idx' not in st.session_state:
    st.session_state.player_idx = 1

if 'num_building' not in st.session_state:
    st.session_state.num_building = 0
    
if 'num_pieces' not in st.session_state:
    st.session_state.num_pieces = 0
    
if 'prev_I' not in st.session_state:
    st.session_state.prev_I = 1
    
if 'resource_automating_counter' not in st.session_state:
    st.session_state.resource_automating_counter = {1:dict(), 2:dict(), 3:dict(), 4:dict()}
    
global_player_resource_dict = st.session_state.player_resource_dict
global_player_addresource_dict = st.session_state.player_addresource_dict
player_idx = st.session_state.player_idx

if 'resource_to_cost_mapping' not in st.session_state:
    st.session_state.resource_to_cost_mapping = {'wood':50, 'iron ore':100, 'gold':750, 'crude oil':750, 'fish':40, 'crop':40, 'meat':100, 'stone':50, 'coal':200, 'animal':50, 'steel':400, 'fine iron':300, 'gasoline':1000, 'food':150, 'building material':600}

if 'prev_p' not in st.session_state:
    st.session_state.prev_p = 0

if 'first_round' not in st.session_state:
    st.session_state.first_round = True
    
processing_plant_product_price_constant = {'steel':3, 'fine iron':2, 'gasoline':2, 'food':2, 'building material':2}

class resource: 
    #Initialize give how many, give what and what is the cost of that resource
    def __init__(self, label, amount, build_cost, little=False):
        self.label = label
        self.amount = amount
        self.little = little
        self.build_cost = build_cost
        
    def display_title(self):
        st.subheader(f'{self.label.capitalize()} Resource')
    
    def display_build(self):
        if not self.little:
            st.button(f'Build {self.label} Collection', on_click=self.build)

    def build(self):
        player_res = st.session_state.player_resource_dict[player_idx]
        if player_res['money'] >= self.build_cost:
            st.session_state.player_resource_dict[player_idx]['money'] -= self.build_cost
            

    def display_button(self):
        print(self.little, self.label)
        if not self.little:
            st.button(f'Get {self.label}', on_click=self.add_player_resource)
        else:
            st.button(f'Get {self.label} (little)', on_click=self.add_player_resource)
    
    def display_generate_resource(self):
        st.write(f'Generates: {self.label}*{self.amount}')
    
    def add_player_resource(self):
        global global_player_resource_dict
        player_resource = global_player_resource_dict[player_idx]
        
        if self.label in player_resource:
            player_resource[self.label] += self.amount
            
        else:
            player_resource[self.label] = self.amount
        
        global_player_resource_dict[player_idx] = player_resource
        st.session_state.player_resource_dict = global_player_resource_dict

class processing_plant:
    #Initialize name and resource needed to build this processing plant
    def __init__(self, required_resource_map:dict, accept_resource_list, product, title=None):
        self.required_resource_map = required_resource_map
        self.accept_resource_list = accept_resource_list
        self.product = product
        self.stored_res_and_amount = dict()
        self.title = title if title is not None else product
        
        
    def display_title(self):
        st.subheader(f'{self.title.capitalize()} Processing Plant')
    

    def display_build_button(self):
        st.button(f'Build {self.product.capitalize()} Processing Plant', on_click=self.build)

    def display_invest_button(self):
        st.button(f'Invest resource to {self.title.capitalize()} Processing Plant', on_click=self.invest)
    
    def display_required_resource(self):
        st.write('Required resource:')
        for key, value in self.required_resource_map.items():
            st.write(f'{key}:{value}')
            
    def build(self):
        global global_player_resource_dict
        player_resource = deepcopy(global_player_resource_dict[player_idx])
        ok = True
        
        constant = 0.9 if option == '慈禧' else 1
        for res_name, amount in self.required_resource_map.items():
            amount = round(amount * build_constant_mapping[option], 1)
            if res_name in player_resource:
                if player_resource[res_name] >= amount*constant:
                    player_resource[res_name] -= amount*constant
                    
                else: #Do not have enough
                    print('Do not have enough')
                    ok = False
            
            else: #Do not have the resource
                print('Do not have enough')
                ok = False
        if ok:
            global_player_resource_dict[player_idx] = player_resource
            st.session_state.player_resource_dict = global_player_resource_dict
           
    def invest(self): #Invest what resource, and how much
        global global_player_resource_dict
        global global_player_addresource_dict
        player_resource = global_player_resource_dict[player_idx]
        next_round_add_resource = global_player_addresource_dict[player_idx]
        ok = True
        
        for key, value in self.stored_res_and_amount.items():
            if value == 0: continue
            elif key not in player_resource or player_resource[key] < value:
                ok = False
                break
        
                
        if ok:
            invested_amount = 0
            for key, value in self.stored_res_and_amount.items():
                if value == 0: continue
                invested_amount += st.session_state.resource_to_cost_mapping[key]*value
                player_resource[key] -= value
            
            invested_amount *= processing_plant_product_price_constant[self.product]
            num_product = invested_amount/st.session_state.resource_to_cost_mapping[self.product]
            
            if self.product in next_round_add_resource:
                next_round_add_resource[self.product] += round(num_product)
            else:
                next_round_add_resource[self.product] = round(num_product)

            
            global_player_addresource_dict[player_idx] = next_round_add_resource
            st.session_state.player_addresource_dict = global_player_addresource_dict
            global_player_resource_dict[player_idx] = player_resource
            st.session_state.player_resource_dict = global_player_resource_dict
            st.session_state.num_building += 1
            self.stored_res_and_amount = dict()
        else:
            print('Not enough resource')
        
class piece:
    def __init__(self, cost, name):
        self.cost = cost
        self.name = name
        
    def display_buy_button(self):
        st.button(f'Buy {self.name} piece', on_click=self.buy)
        
    def buy(self):
        global global_player_resource_dict
        player_resource = deepcopy(global_player_resource_dict[player_idx])
        ok = True
        
        if player_resource['money'] >= self.cost:
            player_resource['money'] -= self.cost
            
        else:
            ok = False
            
        if ok:
            global_player_resource_dict[player_idx] = player_resource
            st.session_state.player_resource_dict = global_player_resource_dict
            st.session_state.num_pieces += 1

class collecting_plant:
    def __init__(self, cost, name, res_name):
        self.cost = cost
        self.name = name
        self.res_name = res_name
    
    def display_button(self):
        st.button(label=f'Buy {self.name} Collection', on_click=self.buy)

    def buy(self):
        global global_player_resource_dict
        player_resource = deepcopy(global_player_resource_dict[player_idx])
        ok = True
        res_name = self.name.lower()
        amount_generated_by_plant = {'wood':20, 'iron ore':10, 'gold':5, 'crude oil':7, 'fish':20, 'crop':20, 'meat':15, 'stone':20, 'coal':20, 'animal':20}
        
        if player_resource['money'] >= self.cost:
            player_resource['money'] -= self.cost
            
        else:
            ok = False
            
        if ok:
            global_player_resource_dict[player_idx] = player_resource
            st.session_state.player_resource_dict = global_player_resource_dict
            
            if self.name not in st.session_state.resource_automating_counter[player_idx]:
                st.session_state.resource_automating_counter[player_idx][self.res_name] = 1
                
            else:
                
                st.session_state.resource_automating_counter[player_idx][self.res_name] += 1
                
            global global_player_addresource_dict
            next_round_add_resource = global_player_addresource_dict[player_idx]
            if res_name not in next_round_add_resource:
                next_round_add_resource[res_name] = st.session_state.resource_automating_counter[player_idx][self.res_name] * amount_generated_by_plant[self.res_name]
                
            else:
                next_round_add_resource[res_name] += st.session_state.resource_automating_counter[player_idx][self.res_name] * amount_generated_by_plant[self.res_name]
            global_player_addresource_dict[player_idx] = next_round_add_resource
            st.session_state.player_addresource_dict = global_player_addresource_dict
def generate_player_info(player_idx):
    player_resource = global_player_resource_dict[player_idx]
        
    result = f'Player {player_idx} resource: | '
    
    for key, value in player_resource.items():
        result += f'{key}:{value}'
        result += ' | '
        
    return result

bottom_right_style = """
    position: fixed;
    bottom: 0;
    left: 0;
    padding: 10px;
    color:green;
    font-size:20px;
    bold:true;
"""

def buy_insurance():
    cost = 500
    global global_player_resource_dict
    player_resource = deepcopy(global_player_resource_dict[player_idx])
    ok = True
    
    if player_resource['money'] >= cost:
        player_resource['money'] -= cost
        
    else:
        ok = False
        
    if ok:
        global_player_resource_dict[player_idx] = player_resource
        st.session_state.player_resource_dict = global_player_resource_dict
    
    
player_string = generate_player_info(player_idx)
st.markdown("<div style='" + bottom_right_style + f"'>{player_string}</div>", unsafe_allow_html=True)

def sell(res_name):
    global global_player_resource_dict
    player_resource = global_player_resource_dict[player_idx]
        
    if res_name in player_resource and player_resource[res_name] > 0:
        player_resource[res_name] -= 1
        money_profit = st.session_state.resource_to_cost_mapping[res_name]
        
        player_resource['money'] += money_profit * income_constant_mapping[option]
        
    global_player_resource_dict[player_idx] = player_resource
    st.session_state.player_resource_dict = global_player_resource_dict

def next_player():
    global player_idx
    global global_player_resource_dict
    
    player_resource = global_player_resource_dict[player_idx]
    next_round_add_resource = global_player_addresource_dict[player_idx]
    
    if st.session_state.player_resource_dict[player_idx]['money'] < 400:
        st.session_state.player_resource_dict[player_idx]['money'] = 0
        
    else:
        st.session_state.player_resource_dict[player_idx]['money'] -= 400
    
    constant = 1.75 if option == '爱迪生' else 1
    for key, value in next_round_add_resource.items():
        if key in player_resource:
            player_resource[key] += round(value*constant)
        else:
            player_resource[key] = round(value*constant)
    
    global_player_resource_dict[player_idx] = player_resource
    st.session_state.player_resource_dict = global_player_resource_dict
    
    char_list = ('爱迪生', '特斯拉', '慈禧', '尼古拉斯二世', '袁隆平', '成吉思汗', '秦始皇', '明治天皇', '罗斯福', '刘秀', '奥本海默', '腓特烈二世')
    char_idx_li = list(st.session_state.char_idx_tuple)
    char_idx_li[player_idx-1] = char_list.index(option)
    tup = tuple(char_idx_li)
    st.session_state.char_idx_tuple = tup
    
    
    player_idx += 1
    if player_idx > 4:
        player_idx = 1
        

    st.session_state.player_idx = player_idx
    st.session_state.player_addresource_dict[player_idx] = dict()
    
def calculate_and_adjust_value_by_inflation_rate():
    cash = 0
    resource_total_cost = 0
    prev_I = st.session_state.prev_I
    
    for _, player_resource_dict in st.session_state.player_resource_dict.items():
        for key, value in player_resource_dict.items():
            if key == 'money':
                cash += value
            else:
                resource_total_cost += st.session_state.resource_to_cost_mapping[key] * value
    
    resource_total_cost *= prev_I 
    num_building = st.session_state.num_building
    num_pieces = st.session_state.num_pieces
    total_money_value = resource_total_cost + cash + num_building + num_pieces
    cur_p = total_money_value/4
    
    prev_p = cur_p*0.95 if st.session_state.prev_p == 0 else st.session_state.prev_p

    constant = random.choice([1, -1])
    cur_I = (((prev_p-cur_p)/prev_p) * constant)*2

    res_to_cost_mapping = st.session_state.resource_to_cost_mapping
    for key, value in res_to_cost_mapping.items():
        res_to_cost_mapping[key] = round(value * (1+cur_I), 0)
        
    st.session_state.prev_I = cur_I
    st.session_state.resource_to_cost_mapping = res_to_cost_mapping
    st.session_state.prev_p = cur_p
    
def count_killed_pieces():
    if option == '成吉思汗':
        st.session_state.player_resource_dict[player_idx]['money'] += 350
        
if player_idx == 1 and st.session_state.first_round:
    calculate_and_adjust_value_by_inflation_rate()
    st.session_state.first_round = False
    
    


with col1:
    
    option = st.selectbox(
        "角色",
        ('爱迪生', '特斯拉', '慈禧', '尼古拉斯二世', '袁隆平', '成吉思汗', '秦始皇', '明治天皇', '罗斯福', '刘秀', '奥本海默', '腓特烈二世'),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        index = st.session_state.char_idx_tuple[st.session_state.player_idx-1]
    )

    
    wood_res = resource('wood', 3, 500)
    wood_res.display_title()
    wood_res.display_build()
    wood_res.display_generate_resource()
    wood_res.display_button()
    st.text("")
    st.text("")
    
    iron_res = resource('iron ore', 2, 750)
    iron_res.display_title()
    iron_res.display_build()
    iron_res.display_generate_resource()
    iron_res.display_button()
    st.text("")
    st.text("")
    
    gold_res = resource('gold', 1, 2500)
    gold_res.display_title()
    gold_res.display_build()
    gold_res.display_generate_resource()
    gold_res.display_button()
    st.text("")
    st.text("")
    
    crude_res = resource('crude oil', 1, 2000)
    crude_res.display_title()
    crude_res.display_build()
    crude_res.display_generate_resource()
    crude_res.display_button()
    st.text("")
    st.text("")
    
    fish_res = resource('fish', 3, 400)
    fish_res.display_title()
    fish_res.display_build()
    fish_res.display_generate_resource()
    fish_res.display_button()
    st.text("")
    st.text("")
    
    crop_res = resource('crop', 3, 400)
    crop_res.display_title()
    crop_res.display_build()
    crop_res.display_generate_resource()
    crop_res.display_button()
    st.text("")
    st.text("")
    
    meat_res = resource('meat', 2, 300)
    meat_res.display_title()
    meat_res.display_build()
    meat_res.display_generate_resource()
    meat_res.display_button()
    st.text("")
    st.text("")
    
    stone_res = resource('stone', 3, 300)
    stone_res.display_title()
    stone_res.display_build()
    stone_res.display_generate_resource()
    stone_res.display_button()
    st.text("")
    st.text("")

    coal_res = resource('coal', 3, 1000)
    coal_res.display_title()
    coal_res.display_build()
    coal_res.display_generate_resource()
    coal_res.display_button()
    st.text("")
    st.text("")
    
    animal_res = resource('animal', 3, 500)
    animal_res.display_title()
    animal_res.display_build()
    animal_res.display_generate_resource()
    animal_res.display_button()
    st.text("")
    st.text("")
    
    wood_res = resource('wood', 1, 0, True)
    wood_res.display_title()
    wood_res.display_generate_resource()
    wood_res.display_button()
    st.text("")
    st.text("")
    
    iron_res = resource('iron ore', 1, 0, True)
    iron_res.display_title()
    iron_res.display_generate_resource()
    iron_res.display_button()
    st.text("")
    st.text("")
    
    gold_res = resource('gold', 1, 0, True)
    gold_res.display_title()
    gold_res.display_generate_resource()
    gold_res.display_button()
    st.text("")
    st.text("")
    
    crude_res = resource('crude oil', 1, 0, True)
    crude_res.display_title()
    crude_res.display_generate_resource()
    crude_res.display_button()
    st.text("")
    st.text("")
    
    fish_res = resource('fish', 1, 0, True)
    fish_res.display_title()
    fish_res.display_generate_resource()
    fish_res.display_button()
    st.text("")
    st.text("")
    
    crop_res = resource('crop', 1, 0, True)
    crop_res.display_title()
    crop_res.display_generate_resource()
    crop_res.display_button()
    st.text("")
    st.text("")
    
    meat_res = resource('meat', 1, 0, True)
    meat_res.display_title()
    meat_res.display_generate_resource()
    meat_res.display_button()
    st.text("")
    st.text("")
    
    stone_res = resource('stone', 1, 0, True)
    stone_res.display_title()
    stone_res.display_generate_resource()
    stone_res.display_button()
    st.text("")
    st.text("")

    coal_res = resource('coal', 1, 0, True)
    coal_res.display_title()
    coal_res.display_generate_resource()
    coal_res.display_button()
    st.text("")
    st.text("")
    
    animal_res = resource('animal', 1, 0, True)
    animal_res.display_title()
    animal_res.display_generate_resource()
    animal_res.display_button()
    st.text("")
    st.text("")

with col2:
    #Steel plant
    steel_dict = dict()
    steel_plant = processing_plant({'money':1500}, ['fine iron', 'coal'], 'steel')
    steel_plant.display_title()
    steel_plant.display_required_resource()
    steel_plant.display_build_button()
    fine_iron_for_steel_plant = st.number_input("Number of fine iron to invest to steel plant:", value=0, placeholder="Type a number...")
    coal_for_steel_plant = st.number_input("Number of coal to invest to steel plant", value=0, placeholder="Type a number...")
    steel_dict['fine iron'] = fine_iron_for_steel_plant
    steel_dict['coal'] = coal_for_steel_plant
    steel_plant.stored_res_and_amount = steel_dict
    steel_plant.display_invest_button()
    st.write('')
    st.write('')
    
    #Steel plant
    fine_iron_dict = dict()
    fine_iron_plant = processing_plant({'money':1000}, ['iron ore'], 'fine iron')
    fine_iron_plant.display_title()
    fine_iron_plant.display_required_resource()
    fine_iron_plant.display_build_button()
    iron_ore_for_fine_iron_plant = st.number_input("Number of iron ore to invest to fine iron plant:", value=0, placeholder="Type a number...")
    fine_iron_dict['iron ore'] = iron_ore_for_fine_iron_plant
    fine_iron_plant.stored_res_and_amount = fine_iron_dict
    fine_iron_plant.display_invest_button()
    st.write('')
    st.write('')
    
    #Refinery plant
    refinery_dict = dict()
    refinery_plant = processing_plant({'money':2000}, ['crude oil'], 'gasoline', 'refinery')
    refinery_plant.display_title()
    refinery_plant.display_required_resource()
    refinery_plant.display_build_button()
    crude_oil_for_refinery_plant = st.number_input("Number of crude oil to invest to refinery plant:", value=0, placeholder="Type a number...")
    refinery_dict['crude oil'] = crude_oil_for_refinery_plant
    refinery_plant.stored_res_and_amount = refinery_dict
    refinery_plant.display_invest_button()
    st.write('')
    st.write('')
    
    #Food plant
    food_dict = dict()
    food_plant = processing_plant({'money':1200}, ['fish', 'crop', 'meat'], 'food')
    food_plant.display_title()
    food_plant.display_required_resource()
    food_plant.display_build_button()
    fish_for_food_plant = st.number_input("Number of fish to invest to food plant:", value=0, placeholder="Type a number...")
    crop_for_food_plant = st.number_input("Number of crop to invest to food plant:", value=0, placeholder="Type a number...")
    meat_for_food_plant = st.number_input("Number of meat to invest to food plant:", value=0, placeholder="Type a number...")
    food_dict['fish'] = fish_for_food_plant
    food_dict['crop'] = crop_for_food_plant
    food_dict['meat'] = meat_for_food_plant
    food_plant.stored_res_and_amount = food_dict
    food_plant.display_invest_button()
    st.write('')
    st.write('')
    
    #Building material
    building_material_dict = dict()
    building_material_plant = processing_plant({'money':1000}, ['wood', 'stone', 'fine iron'], 'building material')
    building_material_plant.display_title()
    building_material_plant.display_required_resource()
    building_material_plant.display_build_button()
    wood_for_building_material_plant = st.number_input("Number of wood to invest to building plant:", value=0, placeholder="Type a number...")
    stone_for_building_material_plant = st.number_input("Number of stone to invest to building plant:", value=0, placeholder="Type a number...")
    fine_iron_for_building_material_plant = st.number_input("Number of fine iron to invest to building plant:", value=0, placeholder="Type a number...")
    building_material_dict['wood'] = wood_for_building_material_plant
    building_material_dict['stone'] = stone_for_building_material_plant
    building_material_dict['fine iron'] = fine_iron_for_building_material_plant
    building_material_plant.stored_res_and_amount = building_material_dict
    building_material_plant.display_invest_button()
    st.write('')
    st.write('')

with col3:
    for res in st.session_state.resource_to_cost_mapping:
        st.button(f'Sell {res}', on_click=sell, args=(res,))

with col4:
    castle_piece = piece(500, 'castle')
    castle_piece.display_buy_button()
    
    bishop_piece = piece(300, 'bishop')
    bishop_piece.display_buy_button()
    
    knight_piece = piece(300, 'knight')
    knight_piece.display_buy_button()
    
    soldier_piece = piece(300, 'soldier')
    soldier_piece.display_buy_button()
    
    st.button('Buy insurance', on_click=buy_insurance)
    
    wood_collect = collecting_plant(500, 'Wood', 'wood')
    wood_collect.display_button()
    
    iron_collect = collecting_plant(750, 'Iron', 'iron ore')
    iron_collect.display_button()
    
    gold_collect = collecting_plant(2500, 'Gold', 'gold')
    gold_collect.display_button()
    
    crude_collect = collecting_plant(2000, 'Crude oil', 'crude oil')
    crude_collect.display_button()
    
    fish_collect = collecting_plant(400, 'Fishing', 'fish')
    fish_collect.display_button()
    
    plant_collect = collecting_plant(400, 'Agriculture', 'crop')
    plant_collect.display_button()
    
    hunt_collect = collecting_plant(300, 'Hunting', 'meat')
    hunt_collect.display_button()
    
    stone_collect = collecting_plant(300, 'Stone', 'stone')
    stone_collect.display_button()
    
    coal_collect = collecting_plant(1000, 'Coal', 'coal')
    coal_collect.display_button()
    
    animal_collect = collecting_plant(500, 'Animal', 'animal')
    animal_collect.display_button()
    
   
with col5:
    st.button('Killed a piece', on_click=count_killed_pieces)
    st.button('Next player', on_click=next_player)
    
