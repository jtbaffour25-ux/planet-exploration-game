import streamlit as st


if "fuel" not in st.session_state:
    st.session_state.fuel = 110

if "current_planet" not in st.session_state:
    st.session_state.current_planet = "Earth"

if "required_resources" not in st.session_state:
    st.session_state.required_resources = {
        "Water": False,
        "Energy": False,
        "Medicine": False,
        "Food": False
    }

if "mission_log" not in st.session_state:
    st.session_state.mission_log = []

st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 900px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

planets = {
    "Earth": {
        "Mars": 8, 
        "Venus": 10,
        "Uranus": 22,
        "Pluto": 16
        
    },
    
     "Mars": {
        "Earth":8,
        "Jupiter": 11,
        "Titan": 18,
        "Saturn": 14, 
        "Mercury": 6
        
    },
     
     "Uranus": {
        "Earth": 22, 
        "Pluto": 11
    },
    
    "Pluto": {
    "Saturn": 15,
    "Neptune": 8,
    "Uranus": 11    
    },
    
    "Jupiter": {
    "Mars": 12, 
    "Saturn": 7,
    "Titan": 9
        
    },
    
    "Titan": {
        "Mars": 18,
        "Jupiter": 9,
        "Saturn": 4,
        "Neptune": 16
    },
    
    "Saturn": {
        "Jupiter": 7,
        "Titan": 4,
        "Pluto": 15
    },
    
    "Mercury": {
        "Mars": 6,
        "KELT-9b": 12
    },
    
     "Neptune": {
        "Venus": 14,
        "Titan": 16,
        "Pluto": 8,
        "WD 1856+534 b": 24
    },
    
    "KELT-9b": {
        "Venus": 30,
        "Mercury": 12
    },
    
    "WD 1856+534 b": {
      "Neptune": 24,
      "Venus": 15
      
    },
    
    "Venus": {
        "Earth": 10,
        "KELT-9b": 30,
        "WD 1856+534 b" : 15,
        "Neptune": 14
        
    }
}

planet_info = {
    "Earth": {
        "discoveries": [],
        "risk": "Low",
        "visited": True
    },

    "Mars": {
        "discoveries": [
            "Water Ice",
            "Martian Soil",
            "Clay minerals"
        ],
        "risk": "Low",
        "visited": False
    },

    "Venus": {
        "discoveries": [
            "Atmospheric nitrogen",
            "Concentrated solar energy",
            "Carbon dioxide",
            "Sulfuric acid",
            "Corrosive clouds"
        ],
        "risk": "Extreme",
        "visited": False
    },

    "Titan": {
        "discoveries": [
            "Organic molecules",
            "Methane lakes",
            "Prebiotic chemistry"
        ],
        "risk": "Medium",
        "visited": False
    },

    "Neptune": {
        "discoveries": [
            "Microbial compound",
            "Methane ice clouds",
            "Extreme wind data"
        ],
        "risk": "High",
        "visited": False
    },

    "Pluto": {
        "discoveries": [
            "Frozen nitrogen",
            "Ancient ice samples"
        ],
        "risk": "Medium",
        "visited": False
    },

    "Uranus": {
        "discoveries": [
            "Methane atmosphere",
            "hazardous gases"
        ],
        "risk": "Medium",
        "visited": False
    },

    "Jupiter": {
        "discoveries": [
            "Hydrogen",
            "Helium",
            "Magnetic field data"
        ],
        "risk": "High",
        "visited": False
    },

    "Saturn": {
        "discoveries": [
            "Iron",
            "Nickel",
            "Atmospheric hydrogen"
        ],
        "risk": "High",
        "visited": False
    },

    "Mercury": {
        "discoveries": [
            "Metal rich crust",
            "Solar radiation data"
        ],
        "risk": "High",
        "visited": False
    },

    "KELT-9b": {
        "discoveries": [
            "Ionized metals",
            "Ultra hot atmosphere data"
        ],
        "risk": "Extreme",
        "visited": False
    },

    "WD 1856+534 b": {
        "discoveries": [
            "White dwarf survival data",
            "Orbital stability research"
        ],
        "risk": "Extreme",
        "visited": False
    }
}

discovery_to_resource = {
    "Water Ice": "Water",
    "Ancient ice samples": "Water",
    "Concentrated solar energy": "Energy",
    "Microbial compound": "Medicine",
    "Organic molecules": "Food"
}

risk_penalty = {
    "Low": 0,
    "Medium": 5,
    "High": 10,
    "Extreme": 20
}

def show_failed_screen(message):
    st.markdown(
        f"""
        <div style="height: 85vh; width: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; background: black; text-align: center;">
            <h1 style="color: #b00000; font-size: 110px; font-family: serif; letter-spacing: 6px;">FAILED!</h1>
            <p style="color: white; font-size: 24px; margin-top: 10px;">{message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if (
    st.session_state.current_planet == "Earth"
    and all(st.session_state.required_resources.values())
):
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            max-width: 100%;
        }
        </style>

        <div style="
            height: 85vh;
            width: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: black;
        ">
            <h1 style="
                color: #00ff41;
                font-size: 120px;
                font-family: monospace;
                letter-spacing: 10px;
                text-shadow: 0 0 15px #00ff41;
                text-align: center;
            ">
                YOU WIN!
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Play Again"):
            st.session_state.clear()
            st.rerun()

    st.stop()

def dijkstra(graph, start):
    import heapq

    distances = {}

    for planet in graph:
        distances[planet] = float("inf")

    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_planet = heapq.heappop(priority_queue)

        if current_distance > distances[current_planet]:
            continue

        for neighbor, weight in graph[current_planet].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances


distances_to_home = dijkstra(planets, st.session_state.current_planet)
cost_to_return_home = distances_to_home["Earth"]

if st.session_state.fuel <= 0:
    show_failed_screen("You ran out of fuel during the mission.")

    if st.button("Restart Mission"):
        st.session_state.clear()
        st.rerun()

    st.stop()

if (
    st.session_state.current_planet != "Earth"
    and st.session_state.fuel < cost_to_return_home
    and not all(st.session_state.required_resources.values())
):
    show_failed_screen("You became stranded before collecting all required resources.")

    if st.button("Restart Mission"):
        st.session_state.clear()
        st.rerun()

    st.stop()


if (
    st.session_state.current_planet != "Earth"
    and st.session_state.fuel < cost_to_return_home
    and all(st.session_state.required_resources.values())
):
    show_failed_screen("You found all required resources, but became stranded before returning to Earth. Humanity never received the supplies.")

    if st.button("Restart Mission"):
        st.session_state.clear()
        st.rerun()

    st.stop()

st.title("Planet Exploration Mission")

st.write("Humanity is dying. Find water, energy, medicine, and food and return to Earth.")


st.subheader("Earth Survival Checklist")

st.checkbox("Water", value=st.session_state.required_resources["Water"], disabled=True)

st.checkbox(
    "Energy",
    value=st.session_state.required_resources["Energy"],
    disabled=True
)

st.checkbox(
    "Medicine",
    value=st.session_state.required_resources["Medicine"],
    disabled=True
)

st.checkbox(
    "Food",
    value=st.session_state.required_resources["Food"],
    disabled=True
)


st.metric("Fuel Remaining", st.session_state.fuel)

st.progress(st.session_state.fuel / 110)

st.metric("Current Planet", st.session_state.current_planet)


current_data = planet_info[st.session_state.current_planet]

st.subheader("Planet Information")

st.write("Risk Level:", current_data["risk"])

st.write("Discoveries:")

for discovery in current_data["discoveries"]:
    st.write("-", discovery)

distances_to_home = dijkstra(planets, st.session_state.current_planet)
cost_to_return_home = distances_to_home["Earth"]

st.subheader("Return Status")
    
st.write("Cheapest Cost To Earth:", cost_to_return_home)
st.write("Fuel Remaining:", st.session_state.fuel)
                
if st.session_state.current_planet == "Earth":
    st.info("You are currently on Earth.")
elif st.session_state.fuel >= cost_to_return_home:
    st.success("You currently have enough fuel to return to Earth.")
else:
    st.error("You cannot make it back to Earth.")
    

st.subheader("Available Routes")

available_routes = planets[st.session_state.current_planet]

for planet, cost in available_routes.items():
    if st.button(f"Travel to {planet} - Cost: {cost}"):
        st.session_state.fuel -= cost

        risk = planet_info[planet]["risk"]
        st.session_state.fuel -= risk_penalty[risk]

        st.session_state.current_planet = planet
        st.session_state.mission_log.append(f"Traveled to {planet}")

        for discovery in planet_info[planet]["discoveries"]:
            if discovery in discovery_to_resource:
                resource = discovery_to_resource[discovery]
                st.session_state.required_resources[resource] = True

        st.session_state.message = f"You traveled to {planet}. Travel cost: {cost}. Risk penalty: {risk_penalty[risk]}."
        st.rerun()

if "message" in st.session_state:
    st.success(st.session_state.message)    

if st.button("Restart Mission"):
    st.session_state.clear()
    st.rerun()







