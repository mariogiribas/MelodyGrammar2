import Scale, Notation

def test_read_scales():
    scales = Scale.read_scales("scales.txt")
    for s in scales:
        print([l.name for l in s.to_notes(Notation.Notation.A)])

test_read_scales()
