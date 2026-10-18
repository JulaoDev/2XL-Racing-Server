import os
import random
import json
from typing import Optional, Dict, Any
from fastapi import FastAPI, Request, HTTPException, Query, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="2XL Racing Mirror Server")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(BASE_DIR, "settings.ini")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SAVE_DIR = os.path.join(BASE_DIR, "cloud_saves")

# Ensure cloud saves directory exists
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# Temporary in-memory state for paint and chat room
CURRENT_PAINT = "matte black"
CHAT_HISTORY = [
    {"user": "Rolon Dev", "msg": "Drag Racing mirror server started in Paraguay."},
    {"user": "Collaborator_01", "msg": "Awesome Garage structure is 100% complete."}
]

def patch_and_load_settings():
    """
    Simulates loading and patching the local game settings configuration.
    """
    # Note: In Python, configparser can be used here if settings.ini structure is required.
    # This matches your original logic layout translated to generic configuration workflow.
    print("[SETTINGS] Loading configuration files...")
    return {"Game Components": {"network": "1"}}

# --- AUTHENTICATION & GAME PROFILE ROUTES ---

@app.api_route("/api/v1/auth/login", methods=["POST", "GET"])
async def game_login():
    """
    Authenticates the player profile client connection.
    """
    print("[AUTH] Client is attempting to authenticate player profile...")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "success",
            "token": "dev_token_2xl_racing_9999",
            "user": {
                "id": 2026,
                "username": "Rolon Dev",
                "credits": 999999,
                "level": 50,
                "is_developer": True
            }
        }
    )

@app.get("/api/v1/profile/load")
async def load_profile():
    """
    Delivers detailed garage, unlocked tracks, and player profile state.
    """
    print("[PROFILE] Delivering detailed garage data...")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "success",
            "current_car": "car_race_01",
            "unlocked_tracks": ["track_quarter_mile"],
            "garage": {
                "owned_cars": ["car_race_01", "car_muscle_70"],
                "current_paint": CURRENT_PAINT
            }
        }
    )

# --- CLOUD SAVE ROUTES ---

@app.post("/api/cloudsave/save")
async def cloud_save(request: Request):
    """
    Saves the user's game progress locally, simulating a cloud database backup.
    """
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid JSON body format"
        )
        
    if not data or 'user_id' not in data or 'game_state' not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid save data structure. Missing user_id or game_state."
        )
    
    user_id = data['user_id']
    game_state = data['game_state']
    
    # Save progress to an individual JSON file per user
    user_save_path = os.path.join(SAVE_DIR, f"save_{user_id}.json")
    with open(user_save_path, 'w') as f:
        json.dump(game_state, f, indent=4)
        
    print(f"[CLOUDSAVE] Backup successfully created for user {user_id}")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "success",
            "message": f"Progress successfully backed up for user {user_id}",
            "timestamp": "2026-10-13"
        }
    )

@app.get("/api/cloudsave/load")
async def cloud_load(user_id: str = Query(..., description="The unique player ID")):
    """
    Retrieves the stored cloud progress file for a specific user.
    """
    user_save_path = os.path.join(SAVE_DIR, f"save_{user_id}.json")
    
    # If the user has no saved progress, return a clean initial sync status
    if not os.path.exists(user_save_path):
        print(f"[CLOUDSAVE] No save profile found for user {user_id}. Initializing fresh sync.")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "new_player",
                "message": "No cloud save found. Starting fresh.",
                "game_state": {}
            }
        )
        
    with open(user_save_path, 'r') as f:
        game_state = json.load(f)
        
    print(f"[CLOUDSAVE] Loading cloud profile data for user {user_id}")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "success",
            "user_id": user_id,
            "game_state": game_state
        }
    )

# --- REVERSE ENGINEERING LEGACY GAMEPLAY INTEGRATIONS ---

@app.get("/api/v1/tracks")
async def get_race_tracks():
    """
    Lists legacy campaign and drag racing tracks.
    """
    return {"status": "success", "tracks": ["track_quarter_mile", "track_half_mile", "pro_circuit_01"]}

@app.post("/api/v1/race/pinkslips")
async def process_pink_slips(request: Request):
    """
    Handles vehicle wagering stakes during Pink Slip high-tier events.
    """
    data = await request.json()
    wagered_car = data.get("wagered_car", "unknown")
    outcome = random.choice(["won", "lost"])
    return {
        "status": "success", 
        "event": "pink_slips", 
        "outcome": outcome, 
        "details": f"You {outcome} the race challenge. Wagered car asset processing completed."
    }

@app.get("/api/v1/daily-rewards")
async def get_daily_rewards():
    """
    Calculates dynamic daily login bonus streaks.
    """
    return {"status": "success", "day_streak": 5, "reward": {"credits": 5000, "gold_tokens": 10}}

@app.post("/api/v1/garage/paint")
async def update_car_paint(request: Request):
    """
    Saves cosmetic custom garage colors to persistent instance memory.
    """
    global CURRENT_PAINT
    data = await request.json()
    CURRENT_PAINT = data.get("paint_style", CURRENT_PAINT)
    return {"status": "success", "updated_paint": CURRENT_PAINT}

@app.get("/api/v1/community/chat")
async def get_chat_messages():
    """
    Returns global chat logs backend timeline.
    """
    return {"status": "success", "history": CHAT_HISTORY}

@app.post("/api/v1/community/chat/send")
async def send_chat_message(request: Request):
    """
    Appends new global message packages into backend logs.
    """
    data = await request.json()
    if "user" in data and "msg" in data:
        CHAT_HISTORY.append({"user": data["user"], "msg": data["msg"]})
        return {"status": "success", "chat_sync": True}
    return {"status": "error", "message": "Malformed message package"}

# --- CLOUD SAVE ROUTES ---

@app.post("/api/v1/profile/save")
async def upload_cloud_save(request: Request):
    """
    Receives the player profile game data and writes it to the local SAVE_DIR.
    """
    try:
        # Extracts raw data or JSON sent by the client
        save_data = await request.json()
        
        # Defines the file path using your pre-declared SAVE_DIR
        file_path = os.path.join(SAVE_DIR, "player_profile.json")
        
        # Writes the content locally
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=4)
            
        print("[CLOUD SAVE] Game backup updated successfully.")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "success", "message": "Cloud save backup complete."}
        )
    except Exception as e:
        print(f"[CLOUD SAVE ERROR] Failed to receive file: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "error", "message": "Invalid save structure."}
        )

@app.get("/api/v1/profile/load")
async def download_cloud_save():
    """
    Reads the player profile backup from SAVE_DIR and delivers it to the client.
    """
    file_path = os.path.join(SAVE_DIR, "player_profile.json")
    
    # Checks if a save file exists; if not, sends a default template
    if not os.path.exists(file_path):
        print("[CLOUD SAVE] No backup found. Delivering empty profile structure.")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "new_player", "profile_data": {}}
        )
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
            
        print("[CLOUD SAVE] Player profile backup loaded successfully.")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "success", "profile_data": loaded_data}
        )
    except Exception as e:
        print(f"[CLOUD SAVE ERROR] Failed to read backup: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "message": "Failed to load cloud save."}
        )

# --- GARAGE CHAT LOGIC ---

@app.get("/api/v1/garage/chat")
async def get_chat_history():
    """
    Loads and delivers the live garage chat logs from the local JSON storage.
    """
    # Defines the path to the chat log file
    chat_file = os.path.join(os.path.dirname(__file__), "chat_history.json")
    
    # If the file doesn't exist, delivers a default greeting structure
    if not os.path.exists(chat_file):
        print("[CHAT] History file missing. Delivering default fallback message.")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=[{"user": "System", "msg": "Welcome to the local server chat room."}]
        )
        
    try:
        with open(chat_file, "r", encoding="utf-8") as f:
            chat_logs = json.load(f)
            
        print("[CHAT] Delivering garage message logs to client...")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=chat_logs
        )
    except Exception as e:
        print(f"[CHAT ERROR] Failed to parse logs: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "message": "Failed to load chat history."}
        )

# --- NEW PLAYER REGISTRATION LOGIC ---

@app.post("/api/v1/auth/register")
async def register_new_player(request: Request):
    """
    Registers a new unique player, assigns an incremental ID, 
    and generates their personal cloud save file using the base template.
    """
    try:
        data = await request.json()
        requested_username = data.get("username", "New Racer").strip()
        
        # Paths for our files
        template_path = os.path.join(os.path.dirname(__file__), "player_template.json")
        
        if not os.path.exists(template_path):
            print("[REGISTER ERROR] Base template file missing.")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"status": "error", "message": "Server error: missing profile template."}
            )
            
        # Count existing profiles to assign a new incremental ID
        existing_saves = [f for f in os.listdir(SAVE_DIR) if f.startswith("player_") and f.endswith(".json")]
        new_id = 3000 + len(existing_saves)
        
        # Read the clean template structure
        with open(template_path, "r", encoding="utf-8") as f:
            new_profile = json.load(f)
            
        # Personalize the copy with unique identifier data
        new_profile["player_id"] = new_id
        new_profile["username"] = requested_username
        
        # Save the new independent file
        new_save_file = os.path.join(SAVE_DIR, f"player_{new_id}.json")
        with open(new_save_file, "w", encoding="utf-8") as f:
            json.dump(new_profile, f, indent=4)
            
        print(f"[REGISTRATION] New driver '{requested_username}' registered with ID: {new_id}")
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "status": "success",
                "message": "Registration complete.",
                "player_id": new_id,
                "username": requested_username
            }
        )
    except Exception as e:
        print(f"[REGISTRATION ERROR] Process failed: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "error", "message": "Invalid registration payload."}
        )

# --- PINK SLIPS & GARAGE BETTING LOGIC ---

@app.post("/api/v1/garage/bet/validate")
async def validate_pink_slip_bet(request: Request):
    """
    Validates a Pink Slip race outcome. If the player wins, 
    the opponent's car is permanently transferred to their local garage JSON profile.
    """
    try:
        data = await request.json()
        player_id = data.get("player_id")
        race_won = data.get("race_won", False)
        reward_car_id = data.get("reward_car_id")
        reward_car_name = data.get("reward_car_name", "Won Vehicle")

        if not player_id:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"status": "error", "message": "Missing player_id parameters."}
            )

        # Locates the specific player save file
        file_name = f"player_{player_id}.json" if player_id != 2026 else "player_profile.json"
        file_path = os.path.join(SAVE_DIR, file_name)

        if not os.path.exists(file_path):
            print(f"[BET ERROR] Target save file not found for player: {player_id}")
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"status": "error", "message": "Player save file missing."}
            )

        # Reads the current driver data
        with open(file_path, "r", encoding="utf-8") as f:
            player_profile = json.load(f)

        # Core logic execution for Pink Slip rewards
        if race_won and reward_car_id:
            # Safely gets or initializes the old format or new structure lists
            if "garage" not in player_profile:
                player_profile["garage"] = {}
            if "owned_cars" not in player_profile["garage"]:
                player_profile["garage"]["owned_cars"] = ["car_race_01"]

            # Checks if the driver already owns the wagered car
            if reward_car_id not in player_profile["garage"]["owned_cars"]:
                player_profile["garage"]["owned_cars"].append(reward_car_id)
                print(f"[PINK SLIPS] Player {player_id} WON the bet! Added '{reward_car_name}' to garage.")
                message = f"Bet validated successfully. Vehicle '{reward_car_name}' added to your garage."
            else:
                print(f"[PINK SLIPS] Player {player_id} won, but already owns '{reward_car_name}'.")
                message = "Bet validated. Vehicle already present in your garage collection."
                
            # Increments career stats for won bets
            if "statistics" in player_profile:
                player_profile["statistics"]["races_played"] = player_profile["statistics"].get("races_played", 0) + 1
                player_profile["statistics"]["races_won"] = player_profile["statistics"].get("races_won", 0) + 1
        else:
            print(f"[PINK SLIPS] Player {player_id} LOST the bet or no reward was specified.")
            message = "Bet processed. No vehicle transfer occurred."
            if "statistics" in player_profile:
                player_profile["statistics"]["races_played"] = player_profile["statistics"].get("races_played", 0) + 1

        # Writes the updated parameters back into the local file storage
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(player_profile, f, indent=4)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "success",
                "message": message,
                "garage_snapshot": player_profile.get("garage", {})
            }
        )
    except Exception as e:
        print(f"[BET LOGIC ERROR] System failure during validation: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "message": "Failed to process vehicle wager validation."}
        )

# --- WORKSHOP UPGRADE LOGIC ---

# Fixed price matrix for performance parts (Level 1 -> Level 2 -> Level 3)
UPGRADE_PRICES = {
    "engine":1500,
    "transmission":3500,
    "tires":7500,
    "nitro":15000,
}

@app.post("/api/v1/workshop/upgrade")
async def upgrade_vehicle_part(request: Request):
    """
    Handles mechanical upgrades for the player's currently equipped car.
    Validates currency, deducts costs, and increments upgrade levels in the profile.
    """
    try:
        data = await request.json()
        player_id = data.get("player_id")
        part_to_upgrade = data.get("part")  # Expected: 'engine', 'transmission', 'tires', 'nitro'
        
        if not player_id or part_to_upgrade not in UPGRADE_PRICES:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"status": "error", "message": "Invalid player parameters or invalid part type."}
            )
            
        # Locates the player file
        file_name = f"player_{player_id}.json" if player_id != 2026 else "player_profile.json"
        file_path = os.path.join(SAVE_DIR, file_name)
        
        if not os.path.exists(file_path):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"status": "error", "message": "Target driver file not found."}
            )
            
        with open(file_path, "r", encoding="utf-8") as f:
            player_profile = json.load(f)
            
        # Identifies the active equipped vehicle in the garage
        current_car_id = player_profile.get("current_equipped_car")
        garage_list = player_profile.get("garage", [])
        
        target_car = None
        for car in garage_list:
            if car.get("car_id") == current_car_id:
                target_car = car
                break
                
        if not target_car:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"status": "error", "message": "Equipped vehicle missing from garage collection."}
            )
            
        # Gets the active upgrade level key name
        level_key = f"{part_to_upgrade}_level"
        current_level = target_car.get("upgrades", {}).get(level_key, 1)
        
        # Max tuning limit configuration check
        if current_level >= 4:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"status": "error", "message": f"{part_to_upgrade.capitalize()} is already maxed out."}
            )
            
        # Calculates transaction values based on price index matrix
        price_index = current_level - 1 if part_to_upgrade != "nitro" else current_level
        cost = UPGRADE_PRICES[part_to_upgrade][price_index]
        player_cash = player_profile.get("currency", {}).get("cash", 0)
        
        if player_cash < cost:
            print(f"[WORKSHOP] Upgrade rejected: Player {player_id} lacks funds for {part_to_upgrade} Level {current_level + 1}.")
            return JSONResponse(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                content={"status": "error", "message": "Insufficient cash balance for this performance upgrade."}
            )
            
        # Processes payment transaction and increments mechanics level data
        player_profile["currency"]["cash"] = player_cash - cost
        target_car["upgrades"][level_key] = current_level + 1
        
        print(f"[WORKSHOP] Player {player_id} upgraded {part_to_upgrade} to Level {current_level + 1}. Cost: ${cost}")
        
        # Saves the modified data profile locally
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(player_profile, f, indent=4)
            
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "success",
                "message": f"Successfully tuned {part_to_upgrade} to Level {current_level + 1}.",
                "remaining_cash": player_profile["currency"]["cash"],
                "updated_upgrades": target_car["upgrades"]
            }
        )
    except Exception as e:
        print(f"[WORKSHOP ERROR] Internal failure during upgrade transaction: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "message": "Failed to complete mechanical upgrade process."}
        )

# --- GARAGE PAINT SHOP LOGIC ---

@app.post("/api/v1/garage/paint")
async def buy_vehicle_paint(request: Request):
    """
    Handles cosmetic paint purchases for the currently equipped vehicle.
    Deducts a flat cost of $500 and updates the color string locally.
    """
    try:
        data = await request.json()
        player_id = data.get("player_id")
        new_color = data.get("paint_color", "factory orange").strip()
        
        if not player_id:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"status": "error", "message": "Missing player_id parameters."}
            )
            
        file_name = f"player_{player_id}.json" if player_id != 2026 else "player_profile.json"
        file_path = os.path.join(SAVE_DIR, file_name)
        
        if not os.path.exists(file_path):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"status": "error", "message": "Player profile not found."}
            )
            
        with open(file_path, "r", encoding="utf-8") as f:
            profile = json.load(f)
            
        player_cash = profile.get("currency", {}).get("cash", 0)
        paint_cost = 500
        
        if player_cash < paint_cost:
            print(f"[PAINT] Purchase rejected: Player {player_id} insufficient cash.")
            return JSONResponse(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                content={"status": "error", "message": "Insufficient cash for this custom paint job."}
            )
            
        # Deduct cost and update the paint values inside the profile
        profile["currency"]["cash"] = player_cash - paint_cost
        
        # Updates global status and current equipped car paint if available
        if "garage" in profile and isinstance(profile["garage"], list):
            current_car_id = profile.get("current_equipped_car")
            for car in profile["garage"]:
                if car.get("car_id") == current_car_id:
                    car["current_paint"] = new_color
                    break
                    
        print(f"[PAINT] Player {player_id} changed car paint to '{new_color}'. Balance: ${profile['currency']['cash']}")
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=4)
            
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "success",
                "message": f"Car paint successfully updated to {new_color}.",
                "remaining_cash": profile["currency"]["cash"]
            }
        )
    except Exception as e:
        print(f"[PAINT ERROR] Customization transaction failed: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "message": "Failed to complete paint application process."}
        )

# --- CORS SECURITY BYPASS MIDDLEWARE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =================================================================
# TITLE: 2XL Racing Preservation Server - Emulation Project Backend
# AUTHOR: Rolon & Collaborators
# DESCRIPTION: FastAPI Mirror Backend to Revive Local & Profile Features
# =================================================================

@app.get("/api/Advertisements/0")
async def get_advertisements(placement: str = "prelogin"):
    # Returns a structured dictionary matching native ad delivery templates
    return {"advertisements": [], "status": "ok"}

@app.get("/api/Advertisements/0")
async def get_advertisements(placement: str = "prelogin"):
    # Clear structure for ad response
    return []

@app.get("/api/token/initialize")
async def initialize_token():
    # Full response injection covering old mobile SDK requirements
    return {
        "status": "success",
        "success": True,
        "token": "ParaguayRacerToken2026",
        "authToken": "ParaguayRacerToken2026",
        "access_token": "ParaguayRacerToken2026",
        "tokenString": "ParaguayRacerToken2026",
        "userId": 1,
        "user_id": "1"
    }

@app.get("/api/profile/offline-bypass")
async def offline_bypass():
    # Simulated local propfile data to bypass strict server checks
    # This structure serves as a backup if the token initialization triggers
    return {
        "status": "success",
        "profile_mode": "offline_validated",
        "save_state": "local_fallback",
        "garage_unlock": True
    }
