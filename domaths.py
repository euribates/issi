import math


angles = [i for i in range(0, 361, 6)]
rads = [i * math.pi * 2.0 / 360. for i in angles]
X = [round(math.sin(a)*40.0, 2) for a in rads]
Y = [-round(math.cos(a)*40, 2) for a in rads]
command = 'M'
buff = []
for _x, _y in zip(X, Y):
    print(f'<circle cx="{_x}" cy="{_y}" r="3" fill="grey" />')
    buff.append(f'{command} {_x:.2f} {_y:.2f}')
    command = 'L'
print(' '.join(buff))



'''

    <path d=" M 50 0 A 40 40 0 {{ long_path }} 1 {{ x }} {{ y }}" stroke="#CC6666" stroke-width="9" fill="none">
    <animate
      attributeName="stroke-width"
      values="10;8;9"
      dur="1s">
    </animate>
    </path>
    
    <path d="M 0 0 a 50 50 1 0 1 4 -40"
    stroke="gold"
    stroke-width="5"
    fill="none"
    stroke-linejoin="round">
        <animate 
            attributeName="d"
            from="M 0 0 a 50 50 1 0 1 4 -40"
            to="M 0 0 a 50 50 1 0 1 -39 -8" 
            dur="5s"
            repeatCount="indefinite"
            />
    </path>

    <path d="M 0 -40 L 4 -40 L 8 -39 L 12 -38 L 16 -37 L 20 -35 L 24 -32 L 27 -30 L 30 -27 L 32 -24 L 35 -20 L 37 -16 L 38 -12 L 39 -8 L 40 -4 L 40 0 L 40 4 L 39 8 L 38 12 L 37 16 L 35 20 L 32 24 L 30 27 L 27 30 L 24 32 L 20 35 L 16 37 L 12 38 L 8 39 L 4 40 L 0 40 L -4 40 L -8 39 L -12 38 L -16 37 L -20 35 L -24 32 L -27 30 L -30 27 L -32 24 L -35 20 L -37 16 L -38 12 L -39 8 L -40 4 L -40 0 L -40 -4 L -39 -8 L -38 -12 L -37 -16 L -35 -20 L -32 -24 L -30 -27 L -27 -30 L -24 -32 L -20 -35 L -16 -37 L -12 -38 L -8 -39 L -4 -40" stroke="lime" stroke-width="2" fill="none">

    <animate
      attributeName="d"
      values="M 0 -40 A 4 -40;M 0 -40 A 16 37"
      dur="8s"
      repeatCount="1" />

    </path>

'''
