from difflib import SequenceMatcher

def content_similarity(text1, text2):
    return SequenceMatcher(None, text1, text2).ratio()

def compare_structures(flat_structure1, flat_structure2, use_tolerance, similarity_threshold=0.7):
    print(f"Comparing structures with{'out' if not use_tolerance else ''} tolerance...")
    comparison = []
    match_count = 0
    mismatch_count = 0

    for elem1 in flat_structure1:
        best_match = None
        best_similarity = 0

        for elem2 in flat_structure2:
            similarity = content_similarity(elem1[1], elem2[1])
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = elem2

        if use_tolerance:
            content_matched = best_similarity >= similarity_threshold
        else:
            content_matched = elem1[1] == (best_match[1] if best_match else '')

        comparison.append({
            'Element 1': elem1[0],
            'Content 1': elem1[1],
            'Element 2': best_match[0] if best_match else '',
            'Content 2': best_match[1] if best_match else '',
            'Content Matched': content_matched
        })

        if content_matched:
            match_count += 1
        else:
            mismatch_count += 1

    print(f"Finished comparing structures with{'out' if not use_tolerance else ''} tolerance.")
    return comparison, match_count, mismatch_count
