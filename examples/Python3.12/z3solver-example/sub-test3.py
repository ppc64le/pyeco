# sub-test3.py — Rule-based systems and constraint propagation
from z3 import (
    Int, Bool, Solver, And, Or, Not, Implies, If,
    sat, unsat, Sum, IntVal
)


def main():
    print("=== sub-test3: rule-based systems and constraint propagation ===\n")

    # ------------------------------------------------------------------ #
    # Test 3a: Access-control rule engine                                  #
    # ------------------------------------------------------------------ #
    print("Test 3a: Access-control rules")
    print("  Rules:")
    print("    R1: admin → can_read AND can_write")
    print("    R2: guest → can_read AND NOT can_write")
    print("    R3: banned → NOT can_read AND NOT can_write")

    admin, guest, banned = Bool("admin"), Bool("guest"), Bool("banned")
    can_read, can_write = Bool("can_read"), Bool("can_write")

    s = Solver()

    # Exactly one role assigned
    s.add(Or(admin, guest, banned))
    s.add(Not(And(admin, guest)))
    s.add(Not(And(admin, banned)))
    s.add(Not(And(guest, banned)))

    # Rule encoding
    s.add(Implies(admin, And(can_read, can_write)))
    s.add(Implies(guest, And(can_read, Not(can_write))))
    s.add(Implies(banned, And(Not(can_read), Not(can_write))))

    # Scenario: user is a guest
    s.add(guest)

    result = s.check()
    assert result == sat
    m = s.model()
    print(f"Result:     {result}")
    print(f"  admin={m[admin]}, guest={m[guest]}, banned={m[banned]}")
    print(f"  can_read={m[can_read]}, can_write={m[can_write]}")
    assert bool(m[can_read]) == True
    assert bool(m[can_write]) == False
    print(f"  guest can_read=True: {bool(m[can_read])}")
    print(f"  guest can_write=False: {not bool(m[can_write])}")

    # ------------------------------------------------------------------ #
    # Test 3b: Scheduling — no two tasks overlap on same worker            #
    # ------------------------------------------------------------------ #
    print("\nTest 3b: Scheduling — 3 tasks assigned to 2 workers, no overlap")
    print("  Each task has duration 1, start in [0..4]")
    print("  Tasks on the same worker must not share a time slot")

    t1_start, t2_start, t3_start = Int("t1_s"), Int("t2_s"), Int("t3_s")
    w1, w2, w3 = Bool("w1"), Bool("w2"), Bool("w3")  # True = worker A, False = worker B

    s2 = Solver()

    for ts in (t1_start, t2_start, t3_start):
        s2.add(ts >= 0, ts <= 4)

    # Tasks on the same worker must not overlap (duration = 1, so start times differ)
    # T1 and T2 on same worker -> t1_start != t2_start
    s2.add(Implies(w1 == w2, t1_start != t2_start))
    s2.add(Implies(w1 == w3, t1_start != t3_start))
    s2.add(Implies(w2 == w3, t2_start != t3_start))

    result2 = s2.check()
    assert result2 == sat
    m2 = s2.model()
    t1v = m2[t1_start].as_long()
    t2v = m2[t2_start].as_long()
    t3v = m2[t3_start].as_long()
    w1v = bool(m2[w1])
    w2v = bool(m2[w2])
    w3v = bool(m2[w3])

    print(f"Result:   {result2}")
    print(f"  Task1: worker={'A' if w1v else 'B'}, start={t1v}")
    print(f"  Task2: worker={'A' if w2v else 'B'}, start={t2v}")
    print(f"  Task3: worker={'A' if w3v else 'B'}, start={t3v}")

    # Verify no overlap on same worker
    if w1v == w2v:
        assert t1v != t2v
    if w1v == w3v:
        assert t1v != t3v
    if w2v == w3v:
        assert t2v != t3v
    print(f"  No overlap constraints satisfied: True")

    # ------------------------------------------------------------------ #
    # Test 3c: Configuration validation — mutually exclusive features      #
    # ------------------------------------------------------------------ #
    print("\nTest 3c: Product configuration — feature exclusivity rules")
    print("  feature_A and feature_B are mutually exclusive")
    print("  feature_C requires feature_A")
    print("  At least one feature must be enabled")

    fa, fb, fc = Bool("fa"), Bool("fb"), Bool("fc")
    s3 = Solver()

    s3.add(Not(And(fa, fb)))         # A and B mutually exclusive
    s3.add(Implies(fc, fa))          # C requires A
    s3.add(Or(fa, fb, fc))           # at least one enabled

    # Force: enable C (which should force A and forbid B)
    s3.add(fc)

    result3 = s3.check()
    assert result3 == sat
    m3 = s3.model()
    fav = bool(m3[fa])
    fbv = bool(m3[fb])
    fcv = bool(m3[fc])

    print(f"Result:  {result3}")
    print(f"  fa={fav}, fb={fbv}, fc={fcv}")
    assert fcv == True
    assert fav == True    # C requires A
    assert fbv == False   # A and B mutually exclusive, A is True so B must be False
    print(f"  fc=True (forced):  {fcv}")
    print(f"  fa=True (C→A):     {fav}")
    print(f"  fb=False (¬(A∧B)): {not fbv}")

    # Verify an invalid config is correctly UNSAT
    s3_bad = Solver()
    s3_bad.add(Not(And(fa, fb)))
    s3_bad.add(Implies(fc, fa))
    s3_bad.add(fc)
    s3_bad.add(fb)          # contradicts: fc→fa and ¬(fa∧fb)
    result3_bad = s3_bad.check()
    assert result3_bad == unsat
    print(f"  Invalid config (fc AND fb) correctly UNSAT: {result3_bad == unsat}")

    print("\nsub-test3 completed successfully!")


if __name__ == "__main__":
    main()
