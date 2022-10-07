Title: Fighting FIRe with FIRE: Assessing the Validity of Text-to-Video Retrieval Benchmarks
Slug: multimodal-retrieval-evaluation
Authors: Pedro Rodriguez
Description: Multimodal Retrieval Evaluation

## Abstract

Searching vast troves of videos with textual descriptions is a core multimodal retrieval task. Owing to the lack of a purpose-built dataset for text-to-video retrieval, video captioning datasets have been re-purposed to evaluate models by (1) treating captions as positive matches to their respective videos and (2) all other videos as negatives. However, this methodology leads to a fundamental flaw during evaluation: since captions are marked as relevant *only* to their original video, many alternate videos *also* match the caption, which creates false-negative caption-video pairs. We show that when these false negatives are corrected, a recent state-of-the-art model gains 25% recall points---a difference that threatens the validity of the benchmark itself. To diagnose and mitigate this issue, we annotate and release 683K additional caption-video pairs. Using these, we recompute effectiveness scores for three models on two standard benchmarks (MSRVTT and MSVD). We find that (1) the recomputed metrics are up to 25% recall points higher for the best models, (2) these benchmarks are nearing saturation for Recall@10, (3) caption length (generality) is related to the number of positives, and (4) annotation costs can be mitigated by choosing evaluation sizes corresponding to desired effect size to detect. We recommend retiring these benchmarks in their current form and make recommendations for future text-to-video retrieval benchmarks.

## Citation

Coming soon

## Code

Experimental code is open sourced and available at [github.com/facebookresearch/mm-retrieval-evaluation](https://github.com/facebookresearch/mm-retrieval-evaluation).
Instructions for complete reproduction are in the readme.

## Data

Data associated with the paper is in the [`data` directory of the open source repository](https://github.com/facebookresearch/mm-retrieval-evaluation/tree/main/data), stored in Git LFS.
Documentation for where to download external datasets to is in [`bin/download_data.sh`](https://github.com/facebookresearch/mm-retrieval-evaluation/blob/main/bin/download_data.sh)

## Contact

Please contact <a target="_blank" href="mailto:me@pedro.ai">Pedro Rodriguez at me@pedro.ai</a>
