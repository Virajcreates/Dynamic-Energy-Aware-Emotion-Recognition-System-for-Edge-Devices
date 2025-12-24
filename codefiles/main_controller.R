# ==============================================================================
# FILE: main_controller.R
# ROLE: The "Brain" - Monitors Energy and Controls Python
# ==============================================================================

# --- FIX 1: FORCE THE PATH BEFORE LOADING LIBRARY ---
# We calculate the absolute path to your environment's python.exe
# This prevents R from looking at the Windows Store version.
cwd <- getwd()
python_path <- file.path(cwd, "energy_env", "Scripts", "python.exe")

if (!file.exists(python_path)) {
  stop(paste("CRITICAL ERROR: Could not find Python at:", python_path, 
             "\nMake sure you are running this script from the project folder!"))
}

# Force the environment variable
Sys.setenv(RETICULATE_PYTHON = python_path)

# Now load reticulate
library(reticulate)
use_python(python_path, required = TRUE)

# Verify connection
cat("Python Configured:\n")
print(py_config())

# ------------------------------------------------------------------------------
# 2. LOAD THE PYTHON VISION ENGINE
# ------------------------------------------------------------------------------

# Add current folder to python path
py_run_string("import sys")
py_run_string(paste0("sys.path.append('", cwd, "')"))

# Import the Python file
vision_module <- import("vision_engine")

print("Initializing Python AI Engine (DeepFace)...")
system_instance <- vision_module$EmotionSystem()
print("AI Engine Ready.")

# ------------------------------------------------------------------------------
# 3. HELPER FUNCTION: GET BATTERY STATUS
# ------------------------------------------------------------------------------
get_battery_status <- function() {
  tryCatch({
    output <- system("wmic path Win32_Battery get EstimatedChargeRemaining", intern = TRUE)
    level <- as.numeric(output[2])
    return(level)
  }, error = function(e) {
    return(85) # Dummy value for desktops
  })
}

# ------------------------------------------------------------------------------
# 4. MAIN CONTROL LOOP
# ------------------------------------------------------------------------------
print("Starting Dynamic Energy-Aware Loop... (Press Esc/Ctrl+C to Stop)")

# We use on.exit to ensure cleanup happens even if we crash
on.exit({
  system_instance$release_camera()
  print("System Shutdown.")
})

while(TRUE) {
  # --- STEP A: Read Energy Status ---
  battery_level <- get_battery_status()
  
  # --- STEP B: The "Brain" Decision Logic ---
  if (!is.na(battery_level) && battery_level > 30) {
    current_mode <- "high"
  } else {
    current_mode <- "low"
  }
  
  # --- STEP C: Command Python to Execute ---
  result_list <- system_instance$get_frame_analysis(power_mode = current_mode)
  
  emotion_detected <- result_list[[1]]
  confidence_score <- result_list[[2]]
  
  # --- STEP D: Log output ---
  cat(sprintf(">> Battery: %s%% | Decision: %s | Emotion: %s \n", 
              battery_level, current_mode, emotion_detected))
  
  # --- STEP E: Pacing ---
  if (current_mode == "low") {
    Sys.sleep(0.5) 
  } else {
    Sys.sleep(0.05) 
  }
}