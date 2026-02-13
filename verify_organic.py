import time
import random
from typing import *

# Import from Systemtest
try:
    import core as Systemtest # Alias for compatibility
    from core import (
        HRMSidecar, MetaState, SafeInterpreter, ToolRegistry
    )
except ImportError as e:
    print(f"Import failed: {e}")
    exit(1)

def run_organic_evolution(cycles=30):
    print(f"============================================================")
    print(f"   🧬 FINAL ORGANIC EVOLUTION TEST ({cycles} Cycles)")
    print(f"   Condition: NO SEEDING, STRICT THRESHOLDS, COMPLEX TASKS")
    print(f"============================================================")

    # 1. Initialize System (Clean Slate)
    registry = ToolRegistry() 
    sidecar = HRMSidecar(registry, quick=True, guided=False)
    
    # RIGOROUS CONFIG
    sidecar.synthesizer.max_candidates = 10000
    sidecar.synthesizer.bank_cap = 1000 # Larger bank to allow statistical emergence
    sidecar.synthesizer.max_depth = 4
    
    # Ensure Mutator is empty
    sidecar.mutator.history = [] 
    
    stats = {
        "success": 0,
        "failed": 0,
        "evolutions": 0,
        "challenges_generated": 0
    }

    # Curriculum:
    # Phase A: Basics (Linear) -> Needs +
    # Phase B: Squares (Quadratic) -> Needs * and potentially Op = n*n
    # Phase C: Composition -> Needs Op(Op(n))
    
    tasks = []
    # Phase A
    for a in range(1, 4):
        tasks.append((f"Linear n+{a}", [{'input': i, 'output': i + a} for i in range(5)]))
    # Phase B
    tasks.append(("Square n*n", [{'input': i, 'output': i * i} for i in range(5)]))
    tasks.append(("Square+1 n*n+1", [{'input': i, 'output': i * i + 1} for i in range(5)]))
    tasks.append(("Square+2 n*n+2", [{'input': i, 'output': i * i + 2} for i in range(5)])) # Should trigger reuse
    # Phase C (Hard)
    tasks.append(("Quartic n^4", [{'input': i, 'output': (i * i) * (i * i)} for i in range(5)]))

    # Repeat tasks to fill cycles if needed, or rely on Self-Critic
    task_queue = tasks + tasks + tasks # ample supply
    
    current_io = None
    current_task_name = "Init"

    start_time = time.time()

    for i in range(1, cycles + 1):
        if not current_io:
            if task_queue:
                current_task_name, current_io = task_queue.pop(0)
            else:
                current_task_name = "Random Drill"
                a = random.randint(1, 3)
                current_io = [{'input': n, 'output': n * a} for n in range(5)]

        print(f"\n[Cycle {i}/{cycles}] Task: {current_task_name}")
        print(f"  > Grammar: {list(sidecar.meta_state.abstractions.keys())}")
        
        cycle_start = time.time()
        
        try:
            results = sidecar.synthesizer.synthesize(
                current_io, 
                deadline=time.time() + 15.0, # 15s Organic Deadline
                task_id=f"cycle_{i}"
            )
        except Exception as e:
            print(f"  [Error] Synthesis crashed: {e}")
            results = []

        if results:
            print(f"  [Result] SUCCESS.")
            stats['success'] += 1
            code, ast, k, v = results[0]
            # print(f"    Code: {code}")
            
            # CRITICAL: Self-Critic Intervention
            # If we solved it, can we make it harder?
            if sidecar.critic and random.random() < 0.5:
                print(f"  [Critic] Generator seems comfortable. Injecting Challenge...")
                challenge_io = sidecar.critic.generate_challenge(sidecar.synthesizer)
                if challenge_io:
                    print(f"  [Critic] CHALLENGE INJECTED.")
                    current_io = challenge_io # Next cycle uses this
                    current_task_name = f"Adversarial Challenge"
                    stats['challenges_generated'] += 1
                else:
                    current_io = None # Proceed to next curriculum
            else:
                 current_io = None # Proceed
        else:
            print(f"  [Result] FAILURE.")
            stats['failed'] += 1
            current_io = None # Skip hard task to keep moving

        # Check Evolution
        current_ops = len(sidecar.meta_state.abstractions)
        if current_ops > stats['evolutions']:
            new_ops = current_ops - stats['evolutions']
            print(f"  🌟 [EVOLUTION] System invented {new_ops} new operator(s)!")
            stats['evolutions'] = current_ops

    total_time = time.time() - start_time
    print(f"\n============================================================")
    print(f"   FINAL ORGANIC TEST COMPLETE (Time: {total_time:.2f}s)")
    print(f"============================================================")
    print(f"   Successes: {stats['success']}")
    print(f"   Failures:  {stats['failed']}")
    print(f"   Adversarial Tasks: {stats['challenges_generated']}")
    print(f"   🧬 Grammar Evolutions: {stats['evolutions']}")
    print(f"   Vocabulary: {list(sidecar.meta_state.abstractions.keys())}")
    for name, expr in sidecar.meta_state.abstractions.items():
        print(f"     - {name}: {expr} (Arity {sidecar.meta_state.get_arity(name)})")
    
    if stats['evolutions'] > 0:
        print("\n✅ VERDICT: SPONTANEOUS EVOLUTION CONFIRMED.")
    else:
        print("\n❌ VERDICT: NO EVOLUTION OBSERVED (Bad Logic or Too Strict).")

if __name__ == "__main__":
    run_organic_evolution()
