import sys

def main():
    sw = open("state_weights.txt", 'r')
    lines = sw.readlines()
    sw.close()
    lines = [x.strip() for x in lines if x.strip()]
    init_probs = {}
    state_list = []
    for i in range(2, len(lines)):
        line_parts = lines[i].split()
        s = line_parts[0].strip('"')
        w = float(line_parts[1])
        init_probs[s] = w
        state_list.append(s)
    total_weight = 0
    for prob in init_probs:
        total_weight += init_probs[prob]
    for prob in init_probs:
        init_probs[prob] = init_probs[prob] / total_weight
    sasw = open("state_action_state_weights.txt", 'r')
    lines = sasw.readlines()
    sasw.close()
    lines = [x.strip() for x in lines if x.strip()]
    content = lines[1].split()
    default_val = float(content[3])
    t_probs = {}
    for s in state_list:
        t_probs[s] = {}
    action_set = set()
    for i in range(2, len(lines)):
        line_parts = lines[i].split()
        s1 = line_parts[0].strip('"')
        a = line_parts[1].strip('"')
        s2 = line_parts[2].strip('"')
        w = float(line_parts[3])
        if a not in t_probs[s1]:
            t_probs[s1][a] = {}
        t_probs[s1][a][s2] = w
        action_set.add(a)
    for s1 in state_list:
        for a in action_set:
            if a not in t_probs[s1]:
                t_probs[s1][a] = {}
            for s2 in state_list:
                if s2 not in t_probs[s1][a]:
                    t_probs[s1][a][s2] = default_val
            total_prob = 0
            for s2 in state_list:
                total_prob += t_probs[s1][a][s2]
            for s2 in state_list:
                t_probs[s1][a][s2] = t_probs[s1][a][s2] / total_prob
    sow = open("state_observation_weights.txt", 'r')
    lines = sow.readlines()
    sow.close()
    lines = [x.strip() for x in lines if x.strip()]
    content = lines[1].split()
    default_vals = float(content[3])
    o_probs = {}
    for s in state_list:
        o_probs[s] = {}
    obs_set = set()
    for i in range(2, len(lines)):
        line_parts = lines[i].split()
        s = line_parts[0].strip('"')
        o = line_parts[1].strip('"')
        w = float(line_parts[2])
        o_probs[s][o] = w
        obs_set.add(o)
    for s in state_list:
        for o in obs_set:
            if o not in o_probs[s]:
                o_probs[s][o] = default_vals
        total_prob = 0
        for o in o_probs[s]:
            total_prob += o_probs[s][o]
        for o in o_probs[s]:
            o_probs[s][o] = o_probs[s][o] / total_prob
    oa = open("observation_actions.txt", 'r')
    content4 = oa.readlines()
    oa.close()
    content4 = [x.strip() for x in content4 if x.strip()]
    num_entries = int(content4[1])
    obs_list = []
    act_list = []
    for i in range(2, len(content4)):
        line_parts = content4[i].split()
        if len(line_parts) == 2:
            o = line_parts[0].strip('"')
            a = line_parts[1].strip('"')
            obs_list.append(o)
            act_list.append(a)
        elif len(line_parts) == 1:
            o = line_parts[0].strip('"')
            obs_list.append(o)
    if len(obs_list) - 1 != len(act_list):
        act_list = act_list[:len(obs_list)-1]
    states = state_list
    T = len(obs_list)
    trellis = []
    backptr = []
    for t in range(T):
        trellis.append({})
        backptr.append({})
    for s in states:
        p_obs = 0
        if obs_list[0] in o_probs[s]:
            p_obs = o_probs[s][obs_list[0]]
        trellis[0][s] = init_probs[s] * p_obs
        backptr[0][s] = None
    for t in range(1, T):
        for s in states:
            best_prob = 0
            best_prev = None
            if t-1 < len(act_list):
                a = act_list[t-1]
            else:
                a = None
            for prev_s in states:
                if a != None:
                    trans_prob = t_probs[prev_s][a][s]
                else:
                    trans_prob = 1
                curr_prob = trellis[t-1][prev_s] * trans_prob
                if curr_prob > best_prob:
                    best_prob = curr_prob
                    best_prev = prev_s
            p_obs = 0
            if obs_list[t] in o_probs[s]:
                p_obs = o_probs[s][obs_list[t]]
            trellis[t][s] = best_prob * p_obs
            backptr[t][s] = best_prev
    final_state = None
    max_prob = 0
    for s in states:
        if trellis[T-1][s] > max_prob:
            max_prob = trellis[T-1][s]
            final_state = s
    result = []
    for i in range(T):
        result.append(None)
    result[T-1] = final_state
    for t in range(T-1, 0, -1):
        result[t-1] = backptr[t][result[t]]

    outfile = open("states.txt", 'w')
    outfile.write("states\n")
    outfile.write(str(len(result)) + "\n")
    for s in result:
        outfile.write('"' + s + '"\n')
    outfile.close()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e)
        sys.exit(1)