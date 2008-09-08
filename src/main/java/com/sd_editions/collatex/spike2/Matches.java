package com.sd_editions.collatex.spike2;

import java.util.List;
import java.util.Set;

import com.google.common.collect.Iterables;
import com.google.common.collect.Lists;
import com.google.common.collect.Sets;

public class Matches {
  private final WitnessIndex base;
  private final WitnessIndex witness;

  public Matches(WitnessIndex _base, WitnessIndex _witness) {
    this.base = _base;
    this.witness = _witness;
  }

  // Integers are word codes
  private Set<Integer> matches() {
    Set<Integer> matches = Sets.newLinkedHashSet(base.getWordCodes());
    matches.retainAll(witness.getWordCodes());
    //    System.out.println(matches);
    return matches;
  }

  public List<Integer> getSequenceOfMatchesInBase() {
    return Lists.newArrayList(matches());
  }

  public List<Integer> getSequenceOfMatchesInWitness() {
    return witness.sortMatchesByPosition(matches());
  }

  public List<Gap> getGapsForBase() {
    return getGapsForWitness(base);
  }

  public List<Gap> getGapsForWitness() {
    return getGapsForWitness(witness);
  }

  @SuppressWarnings("boxing")
  private List<Gap> getGapsForWitness(WitnessIndex witnessIndex) {
    int currentIndex = 1;
    List<Integer> positions = witnessIndex.getPositionsOfMatchesInSequence(matches());
    List<Gap> gaps = Lists.newArrayList();
    for (Integer position : positions) {
      int indexDif = position - currentIndex;
      gaps.add(new Gap(witnessIndex, indexDif, currentIndex, position - 1));
      currentIndex = 1 + position;
    }
    int IndexDif = witnessIndex.size() - currentIndex + 1;
    gaps.add(new Gap(witnessIndex, IndexDif, currentIndex, witnessIndex.size()));
    System.out.println(gaps);
    return gaps;
  }

  public List<MisMatch> getMisMatches() {
    List<Gap> gapsForBase = getGapsForBase();
    List<Gap> gapsForWitness = getGapsForWitness();
    List<MisMatch> mismatches = Lists.newArrayList();
    for (int i = 0; i < gapsForBase.size(); i++) {
      Gap _base = gapsForBase.get(i);
      Gap _witness = gapsForWitness.get(i);
      mismatches.add(new MisMatch(_base, _witness));
    }
    return Lists.newArrayList(Iterables.filter(mismatches, new ValidMismatchPredicate())); // TODO: this can be done easier!
  }
}
