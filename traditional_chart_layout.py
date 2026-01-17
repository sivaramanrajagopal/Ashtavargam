#!/usr/bin/env python3
"""
Traditional South Indian Astrology Chart Layout
This provides the correct arrangement of 12 houses in a traditional chart format
"""

def get_traditional_chart_layout():
    """
    Traditional South Indian astrology chart layout:
    - 4 houses in the top row (houses 10, 11, 12, 1)
    - 2 houses on the right side (houses 2, 3)
    - 4 houses in the bottom row (houses 4, 5, 6, 7)
    - 2 houses on the left side (houses 8, 9)
    - Central empty space
    """
    
    # 2D array representation of the traditional chart layout
    # Each position contains the house number
    chart_layout = [
        [None, 10, 11, 12, 1, None],    # Top row
        [9, None, None, None, None, 2],  # Left and right sides
        [8, None, None, None, None, 3],  # Left and right sides
        [None, 7, 6, 5, 4, None]        # Bottom row
    ]
    
    # Alternative representation as a dictionary for easier access
    house_positions = {
        1: (0, 4),   # Row 0, Column 4
        2: (1, 5),   # Row 1, Column 5
        3: (2, 5),   # Row 2, Column 5
        4: (3, 4),   # Row 3, Column 4
        5: (3, 3),   # Row 3, Column 3
        6: (3, 2),   # Row 3, Column 2
        7: (3, 1),   # Row 3, Column 1
        8: (2, 0),   # Row 2, Column 0
        9: (1, 0),   # Row 1, Column 0
        10: (0, 1),  # Row 0, Column 1
        11: (0, 2),  # Row 0, Column 2
        12: (0, 3)   # Row 0, Column 3
    }
    
    return chart_layout, house_positions

def get_chart_css_grid():
    """
    CSS Grid layout for the traditional chart
    """
    css_grid = """
    .traditional-chart {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr;
        grid-template-rows: 1fr 1fr 1fr 1fr;
        gap: 5px;
        max-width: 600px;
        margin: 0 auto;
        background: #f8f9fa;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .chart-house {
        background: white;
        border: 2px solid #dee2e6;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        min-height: 80px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: all 0.3s ease;
    }
    
    .chart-house:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .chart-house.ascendant {
        background: linear-gradient(135deg, #ff6b6b, #ffa500);
        color: white;
        border-color: #ff4757;
    }
    
    .chart-house.planets {
        background: linear-gradient(135deg, #4ecdc4, #44a08d);
        color: white;
        border-color: #26a69a;
    }
    
    .chart-house.empty {
        background: #f8f9fa;
        color: #6c757d;
        border-color: #dee2e6;
    }
    
    .house-number {
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 5px;
    }
    
    .rasi-name {
        font-size: 14px;
        margin-bottom: 8px;
        font-family: 'Tamil', 'Arial Unicode MS', sans-serif;
    }
    
    .planets-list {
        font-size: 12px;
        line-height: 1.2;
    }
    
    .planet-tag {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 2px 6px;
        margin: 1px;
        border-radius: 10px;
        font-size: 10px;
    }
    """
    
    return css_grid

def get_chart_html_template():
    """
    HTML template for the traditional chart
    """
    html_template = """
    <div class="traditional-chart">
        <!-- Top row: Houses 10, 11, 12, 1 -->
        <div class="chart-house" data-house="10">
            <div class="house-number">10</div>
            <div class="rasi-name" id="rasi-10">மகரம்</div>
            <div class="planets-list" id="planets-10"></div>
        </div>
        <div class="chart-house" data-house="11">
            <div class="house-number">11</div>
            <div class="rasi-name" id="rasi-11">கும்பம்</div>
            <div class="planets-list" id="planets-11"></div>
        </div>
        <div class="chart-house" data-house="12">
            <div class="house-number">12</div>
            <div class="rasi-name" id="rasi-12">மீனம்</div>
            <div class="planets-list" id="planets-12"></div>
        </div>
        <div class="chart-house ascendant" data-house="1">
            <div class="house-number">1</div>
            <div class="rasi-name" id="rasi-1">மேஷம்</div>
            <div class="planets-list" id="planets-1"></div>
        </div>
        
        <!-- Right side: Houses 2, 3 -->
        <div class="chart-house" data-house="2">
            <div class="house-number">2</div>
            <div class="rasi-name" id="rasi-2">ரிஷபம்</div>
            <div class="planets-list" id="planets-2"></div>
        </div>
        <div class="chart-house" data-house="3">
            <div class="house-number">3</div>
            <div class="rasi-name" id="rasi-3">மிதுனம்</div>
            <div class="planets-list" id="planets-3"></div>
        </div>
        
        <!-- Left side: Houses 8, 9 -->
        <div class="chart-house" data-house="8">
            <div class="house-number">8</div>
            <div class="rasi-name" id="rasi-8">விருச்சிகம்</div>
            <div class="planets-list" id="planets-8"></div>
        </div>
        <div class="chart-house" data-house="9">
            <div class="house-number">9</div>
            <div class="rasi-name" id="rasi-9">தனுசு</div>
            <div class="planets-list" id="planets-9"></div>
        </div>
        
        <!-- Bottom row: Houses 4, 5, 6, 7 -->
        <div class="chart-house" data-house="4">
            <div class="house-number">4</div>
            <div class="rasi-name" id="rasi-4">கடகம்</div>
            <div class="planets-list" id="planets-4"></div>
        </div>
        <div class="chart-house" data-house="5">
            <div class="house-number">5</div>
            <div class="rasi-name" id="rasi-5">சிம்மம்</div>
            <div class="planets-list" id="planets-5"></div>
        </div>
        <div class="chart-house" data-house="6">
            <div class="house-number">6</div>
            <div class="rasi-name" id="rasi-6">கன்னி</div>
            <div class="planets-list" id="planets-6"></div>
        </div>
        <div class="chart-house" data-house="7">
            <div class="house-number">7</div>
            <div class="rasi-name" id="rasi-7">துலாம்</div>
            <div class="planets-list" id="planets-7"></div>
        </div>
    </div>
    """
    
    return html_template

def get_chart_javascript():
    """
    JavaScript function to populate the traditional chart
    """
    js_code = """
    function populateTraditionalChart(nativeChart) {
        // Clear all planets first
        for (let i = 1; i <= 12; i++) {
            const planetsElement = document.getElementById(`planets-${i}`);
            const rasiElement = document.getElementById(`rasi-${i}`);
            const houseElement = document.querySelector(`[data-house="${i}"]`);
            
            if (planetsElement) planetsElement.innerHTML = '';
            if (houseElement) houseElement.className = 'chart-house';
        }
        
        // Populate each house
        nativeChart.forEach(house => {
            const houseNum = house.house;
            const rasiName = house.rasi_name;
            const planets = house.planets || [];
            
            // Update Rasi name
            const rasiElement = document.getElementById(`rasi-${houseNum}`);
            if (rasiElement) {
                rasiElement.textContent = rasiName;
            }
            
            // Update planets
            const planetsElement = document.getElementById(`planets-${houseNum}`);
            const houseElement = document.querySelector(`[data-house="${houseNum}"]`);
            
            if (planetsElement && houseElement) {
                if (planets.length > 0) {
                    houseElement.className = 'chart-house planets';
                    planetsElement.innerHTML = planets.map(planet => 
                        `<span class="planet-tag">${planet}</span>`
                    ).join('');
                } else {
                    houseElement.className = 'chart-house empty';
                    planetsElement.innerHTML = '<span class="planet-tag">Empty</span>';
                }
            }
        });
        
        // Highlight Ascendant (House 1)
        const ascendantElement = document.querySelector('[data-house="1"]');
        if (ascendantElement) {
            ascendantElement.className = 'chart-house ascendant';
        }
    }
    """
    
    return js_code

if __name__ == "__main__":
    # Test the layout
    layout, positions = get_traditional_chart_layout()
    
    print("Traditional South Indian Astrology Chart Layout:")
    print("=" * 50)
    print("2D Array Layout:")
    for row in layout:
        print(row)
    
    print("\nHouse Positions (row, column):")
    for house, pos in sorted(positions.items()):
        print(f"House {house:2d}: {pos}")
    
    print("\nCSS Grid Template:")
    print(get_chart_css_grid())
