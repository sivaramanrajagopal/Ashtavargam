# Ashtakavarga Popup Implementation

## Overview
Added a new "Ashtakavarga" button and popup modal to the chat interface that displays complete BAV (Bhinnashtakavarga) and SAV (Sarvashtakavarga) calculations in a Prokerala-style format.

## Features Added

### 1. New Header Button
- **Button**: "🔢 Ashtakavarga" button in the chat header
- **Location**: Before "Dasha & Gochara" button
- **State**: Disabled until chat session starts (enabled after birth details are entered)

### 2. Ashtakavarga Modal
- **Size**: Large modal (max-width: 1200px) for comprehensive chart display
- **Content**: Complete BAV/SAV calculations with tabbed interface

### 3. Tabbed Interface
The modal includes tabs for:
- **Individual Planet BAV Charts**: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Ascendant
- **SAV Chart**: Sarvashtakavarga (combined chart)
- **Overall View**: Side-by-side comparison of all BAV charts and SAV

### 4. Chart Rendering
Each planet tab displays:
- **BAV Grid**: 4x4 grid with Prokerala-style layout
  - Fixed RASI positions (South Indian style)
  - Central cell showing planet name and total
  - Color-coded cells (high/medium/low strength)
  - Planet's natural house highlighted
- **BAV Table**: Detailed table showing RASI names and points

### 5. SAV Chart
- **SAV Grid**: 4x4 grid with central merged cell
- **SAV Table**: Shows SAV points per RASI with strength classification
- **Strength Indicators**: Strong (≥30), Good (≥28), Moderate (≥22), Weak (<22)

### 6. Overall Comparison
- **Side-by-side BAV Charts**: All 8 planets displayed in mini-grid format
- **SAV Chart**: Complete SAV visualization
- **Responsive Grid**: Auto-adjusts to screen size

## Technical Implementation

### Files Modified
- `agent_app/templates/chat.html`
  - Added Ashtakavarga button in header
  - Added Ashtakavarga modal HTML
  - Added CSS styles for BAV/SAV grids and tables
  - Added JavaScript functions for fetching and rendering data

### API Integration
- **Endpoint**: `POST /api/v1/calculate/full` (BAV/SAV API)
- **Base URL**: `http://localhost:8000` (configurable via `BAV_SAV_API` constant)
- **Request Format**:
  ```json
  {
    "dob": "YYYY-MM-DD",
    "tob": "HH:MM",
    "latitude": float,
    "longitude": float,
    "tz_offset": float,
    "name": "optional",
    "place": "optional"
  }
  ```

### JavaScript Functions
1. **`openAshtakavargaModal()`**: Opens modal and fetches BAV/SAV data
2. **`renderAshtakavargaModal(data)`**: Main rendering function
3. **`renderBAVSection(planet, chart, ...)`**: Renders individual planet BAV
4. **`renderSAVSection(savChart, ...)`**: Renders SAV chart
5. **`renderOverallSection(...)`**: Renders overall comparison
6. **`showPlanetTab(planet)`**: Tab switching functionality

### CSS Classes
- `.ashtakavarga-container`: Main container
- `.planet-tabs`: Tab navigation
- `.bav-section`: Individual planet sections
- `.bav-grid`: 4x4 grid layout
- `.bav-cell`: Individual grid cells
- `.bav-table`: Data tables
- `.sav-grid`: SAV grid layout
- `.overall-grid`: Overall comparison grid
- `.overall-bav-mini-grid`: Mini BAV grids

## Usage

1. **Start Chat Session**: Enter birth details and click "Start Chat"
2. **Open Ashtakavarga**: Click "🔢 Ashtakavarga" button in header
3. **Navigate Tabs**: Click planet names or "SAV"/"Overall" tabs
4. **View Charts**: See BAV grids, tables, and SAV visualizations
5. **Close Modal**: Click X button, click outside, or press Escape

## Styling
- **Dark Theme**: Matches chat interface dark theme
- **Color Coding**:
  - Green (#10a37f): High strength, active tabs
  - Amber (#f59e0b): Medium strength
  - Red (#ef4444): Low strength
- **Responsive**: Adapts to different screen sizes
- **Prokerala Style**: Matches the original Flask app's Prokerala-style layout

## Error Handling
- Checks if birth data is available before opening modal
- Displays error messages if API is unavailable
- Shows loading indicators during data fetch
- Handles missing or invalid data gracefully

## Future Enhancements
- Add export functionality (PDF/image)
- Add print-friendly view
- Add detailed interpretations per planet
- Add comparison with previous calculations
- Add interactive tooltips for RASI names

