def adjust(old_r, old_g, old_b, shift_k):
  shifted_r = old_r
  shifted_g = old_g
  shifted_b = old_b * shift_k / 100

  return (shifted_r, shifted_g, shifted_b)