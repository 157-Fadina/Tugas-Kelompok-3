import textwrap

rules = [
    {'id': 'R1', 'if': ['Mesin Mati Total'], 'then': 'Cek '
    'Kelistrikan', 'priority': 1, 'desc': 'Rendah'},
    {'id': 'R2', 'if': ['Mesin Berputar Lambat'], 'then': 'Aki '
    'Lemah', 'priority': 2, 'desc': 'Sedang'},
    {'id': 'R3', 'if': ['Lampu Redup'], 'then': 'Aki Lemah', 
     'priority': 2, 'desc': 'Sedang'},
    {'id': 'R4', 'if': ['Aki Lemah', 'Tidak ada Karat pada '
    'Terminal'], 'then': 'Ganti Aki', 'priority': 3, 'desc': 
    'Tinggi'},
    {'id': 'R5', 'if': ['Suara Klik saat Start'], 'then': 'Aki '
    'Lemah', 'priority': 2, 'desc': 'Sedang'},
    {'id': 'R6', 'if': ['Mesin Mati Total', 'Tidak ada '
    'Suara'], 'then': 'Fungsi Kelistrikan Terputus', 'priority': 
    4, 'desc': 'Tinggi (Spesifik)'},
    {'id': 'R7', 'if': ['Aki Lemah'], 'then': 'Mesin Sulit '
    'Start', 'priority': 1, 'desc': 'Rendah'},
    {'id': 'R8', 'if': ['Cek Kelistrikan', 'Terjadi Konsleting'], 
     'then': 'Isolasi Kelistrikan', 'priority': 5, 'desc': 
     'Tertinggi (Order)'}
]

initial_facts = {'Mesin Mati Total', 'Suara Klik saat Start', 
'Tidak ada Karat pada Terminal'}

def forward_chaining(rules, facts):
    """
    Melakukan inferensi data-driven (forward chaining) dan 
    menunjukkan proses
    conflict resolution.
    """
    print("---  Memulai Forward Chaining (Data-Driven) ---")
    print(f"Fakta Awal: {facts}\n")
    
    working_memory = set(facts)
    fired_rules = set()
    iteration = 1
    
    while True:
        print(f"--- Iterasi {iteration} ---")
        
        conflict_set = []
        for rule in rules:
            if rule['id'] in fired_rules:
                continue  
            
            is_match = all(premise in working_memory for premise 
            in rule['if'])
            
            if is_match:
                conflict_set.append(rule)
        
        if not conflict_set:
            print("Tidak ada aturan lagi yang dapat diaktifkan. " 
            "Inferensi selesai.")
            break
            
        print(f"Conflict Set (Aturan yang siap): {[r['id'] for r 
        in conflict_set]}")
        
        selected_rule = sorted(conflict_set, key=lambda r: (-r
        ['priority'], r['id']))[0]
        
        print(f"Resolusi Konflik:")
        for r in sorted(conflict_set, key=lambda r: (-r
        ['priority'], r['id'])):
            status = " terpilih" if r['id'] == selected_rule    
            ['id'] else ""
            print(f"  - {r['id']} (Prioritas: {r['priority']} - {r
            ['desc']}){status}")
        
        new_fact = selected_rule['then']
        
        if new_fact not in working_memory:
            working_memory.add(new_fact)
            print(f"\n ATURAN DIAKTIFKAN: {selected_rule['id']}")
            print(f"==> FAKTA BARU: {new_fact}\n")
        else:
            print(f"\n ATURAN DIAKTIFKAN: {selected_rule['id']}")
            print(f"==> (Fakta '{new_fact}' sudah ada di memori)\n")

        fired_rules.add(selected_rule['id'])
        iteration += 1
        
    print("-------------------------------------------------")
    print(" Kesimpulan Akhir (Semua fakta di Working Memory):")
    print(textwrap.fill(str(working_memory), 80))
    print("-------------------------------------------------")
    return working_memory

def backward_chaining(rules, facts, goal, trace_log):
    """
    Mencoba membuktikan 'goal' menggunakan inferensi goal-driven
    (backward chaining).
    Mengembalikan True jika terbukti, False jika tidak.
    """
    indent = "  " * len(trace_log)
    print(f"{indent} Mencoba membuktikan tujuan: {goal}")
    trace_log.append(goal)

    if goal in facts:
        print(f"{indent} SUKSES: '{goal}' ada di fakta awal.")
        trace_log.pop()
        return True

    rules_that_conclude_goal = [r for r in rules if r['then'] == goal]
    
    if not rules_that_conclude_goal:
        print(f"{indent} GAGAL: Tidak ada aturan yang 
        menghasilkan '{goal}'.")
        trace_log.pop()
        return False

    print(f"{indent} Menemukan {len(rules_that_conclude_goal)} 
    aturan yang menghasilkan '{goal}': {[r['id'] for r in 
    rules_that_conclude_goal]}")

    for rule in rules_that_conclude_goal:
        print(f"{indent}--- Mencoba Aturan {rule['id']} ---")
        all_premises_proven = True
        
        for premise in rule['if']:

            is_premise_proven = backward_chaining(rules, facts, 
            premise, trace_log)
            
            if not is_premise_proven:
                all_premises_proven = False
                print(f"{indent} GAGAL Aturan {rule['id']}: 
                Premis '{premise}' tidak terbukti.")
                break 
        
        if all_premises_proven:
            print(f"{indent} SUKSES Aturan {rule['id']}: Semua 
            premis terbukti.")
            print(f"{indent} SUKSES: Tujuan '{goal}' terbukti.")
            trace_log.pop()
            return True
            
    print(f"{indent} GAGAL: Tujuan '{goal}' tidak dapat 
    dibuktikan setelah mencoba semua aturan.")
    trace_log.pop()
    return False

final_facts = forward_chaining(rules, initial_facts)


print("\n\n---  Memulai Backward Chaining (Goal-Driven) ---")
goal_to_prove = 'Ganti Aki'
print(f"Fakta Awal: {initial_facts}")
print(f"Tujuan (Goal): {goal_to_prove}\n")

trace_log = [] 
is_proven = backward_chaining(rules, initial_facts, goal_to_prove, trace_log)

print("-------------------------------------------------")
print(f"🏁 Hasil Akhir Backward Chaining: Tujuan '{goal_to_prove}'")
print(f"==> {'TERBUKTI' if is_proven else 'TIDAK TERBUKTI'}")
print("-------------------------------------------------")
