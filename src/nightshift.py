r = 255
g = 255
b = 255
k = 50
def color_shift(old_r, old_g, old_b, shift_k):
  shifted_r = old_r
  shifted_g = old_g
  shifted_b = old_b * shift_k / 100

  return [shifted_r, shifted_g, shifted_b]

print(color_shift(r,g,b,k))
