"""
Sorting animations.
"""

from util import *
import random

X = 0
Y = 0
WIDTH = 1920
HEIGHT = 1080
BAR_SPACING = 10
PADDING = 20
FRAMES_PER_IMAGE = 1

pencil = get_pencil("Stroke")
layer = pencil.layers.get("Lines")
bar_mat = create_material(
    "Bar",
    pencil=pencil,
    fill=(177, 186, 177),
    stroke=False
)
bar_mat_index = pencil.materials.find(bar_mat.name)
bar_highlight_mat = create_material(
    "BarHighlight",
    pencil=pencil,
    fill=(75, 104, 189),
    stroke=False
)
bar_highlight_mat_index = pencil.materials.find(bar_highlight_mat.name)
bar_sorted_mat = create_material(
    "BarSorted",
    pencil=pencil,
    fill=(26, 173, 28),
    stroke=False
)
bar_sorted_mat_index = pencil.materials.find(bar_sorted_mat.name)

current_frame = 1
def draw_bars(bars, highlight=None, done=None, pointer=None, max_value=None):
    global current_frame
    if max_value is None:
        max_value = max(bars)
    frame = get_frame(layer, current_frame)
    bar_width = (WIDTH - (PADDING * 2) - ((len(bars) - 1) * BAR_SPACING)) / len(bars)
    height_unit = (HEIGHT - (PADDING * 2)) / (max_value * 1.3)

    if highlight is None:
        highlight = set()
    if done is None:
        done = set()

    for i, bar in enumerate(bars):
        x = PADDING + i * (bar_width + BAR_SPACING)
        y = PADDING
        stroke = draw_rect(frame, (X + x, Y + y), bar_width, bar * height_unit)
        if i in done:
            stroke.material_index = bar_sorted_mat_index
        elif i in highlight:
            stroke.material_index = bar_highlight_mat_index
        else:
            stroke.material_index = bar_mat_index

    if pointer is not None:
        x = PADDING + pointer * (bar_width + BAR_SPACING)
        y = PADDING
        stroke = frame.strokes.new()
        stroke.display_mode = "3DSPACE"
        stroke.points.add(count=4)
        stroke.points[0].co = pt(X + x, Y + y - 10)
        stroke.points[1].co = pt(X + x + bar_width, Y + y - 10)
        stroke.points[2].co = pt(X + x + (bar_width / 2), Y + y + 10)
        stroke.points[3].co = pt(X + x, Y + y - 10)
        stroke.material_index = bar_highlight_mat_index
    current_frame += FRAMES_PER_IMAGE

def selection_sort(numbers):
    draw_bars(numbers)
    length = len(numbers)
    done = set()
    for i in range(length):
        min_index = i
        for j in range(i, length):
            draw_bars(numbers, highlight={j}, done=done, pointer=min_index)
            if numbers[j] < numbers[min_index]:
                min_index = j
        tmp = numbers[min_index]
        numbers[min_index] = numbers[i]
        numbers[i] = tmp
        done.add(i)
        draw_bars(numbers, done=done)

def bubble_sort(numbers):
    draw_bars(numbers)
    length = len(numbers)
    done = set()
    for i in range(length):
        for j in range(length - i - 1):
            draw_bars(numbers, highlight={j, j + 1}, done=done)
            if numbers[j] > numbers[j + 1]:
                tmp = numbers[j]
                numbers[j] = numbers[j + 1]
                numbers[j + 1] = tmp
        done.add(length - i - 1)
    draw_bars(numbers, done=done)

def insertion_sort(numbers):
    draw_bars(numbers)
    length = len(numbers)
    done = set()
    for i in range(length):
        draw_bars(numbers, highlight={i}, done=done)
        done.add(i)
        for j in range(i - 1, -1, -1):
            if numbers[j + 1] < numbers[j]:
                tmp = numbers[j + 1]
                numbers[j + 1] = numbers[j]
                numbers[j] = tmp
                draw_bars(numbers, highlight={j}, done=done - {j})
            else:
                draw_bars(numbers, highlight={j}, done=done - {j})
                break
        draw_bars(numbers, done=done)
    draw_bars(numbers, done=done)
    return numbers

def mergesort(numbers):
    done = set()
    length = len(numbers)
    max_value = max(numbers)
    draw_bars(numbers, max_value=max_value)
    def mergesort_aux(numbers, start, end):
        if end - start <= 1:
            return
        midpoint = int(start + ((end - start) / 2))
        mergesort_aux(numbers, start, midpoint)
        mergesort_aux(numbers, midpoint, end)
        left = numbers[start:midpoint]
        right = numbers[midpoint:end]
        i = start
        while left or right:
            if not right:
                numbers[i] = left[0]
                left = left[1:]
            elif not left:
                numbers[i] = right[0]
                right = right[1:]
            elif left[0] <= right[0]:
                numbers[i] = left[0]
                left = left[1:]
            else:
                numbers[i] = right[0]
                right = right[1:]
            if start == 0 and end == length:
                done.add(i)
            draw_bars(numbers, highlight={i}, max_value=max_value, done=done - {i})
            i += 1
    mergesort_aux(numbers, 0, len(numbers))
    draw_bars(numbers, done=done, max_value=max_value)
    return numbers

def main():
    values = [random.randint(10, 500) for _ in range(40)]
    mergesort(values)
    print(f"Animation Generated. Final Frames: {current_frame}")

if __name__ == "__main__":
    main()
