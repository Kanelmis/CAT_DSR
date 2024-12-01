import sys
from speechbrain.utils import edit_distance


def print_cer_summary(cer_details, file=sys.stdout):
    """Prints out CER summary details in human-readable format.

    This function essentially mirrors the Kaldi compute-wer output format but for CER.

    Arguments
    ---------
    cer_details : dict
        Dict of CER summary details.
    file : stream
        Where to write. (default: sys.stdout)
    """
    print(
        "%CER {CER:.2f} [ {num_edits} / {num_scored_chars}, {insertions} ins, {deletions} del, {substitutions} sub ]".format(
            **cer_details
        ),
        file=file,
        end="",
    )


def print_cer_alignments(
        details_by_utterance,
        file=sys.stdout,
        empty_symbol="<eps>",
        separator=" ; ",
        print_header=True,
        sample_separator=None,
):
    """Print CER summary and alignments.

    Arguments
    ---------
    details_by_utterance : list
        List of CER details by utterance, must include alignments.
    file : stream
        Where to write. (default: sys.stdout)
    empty_symbol : str
        Symbol to use when aligning to nothing.
    separator : str
        String that separates each token in the output.
    print_header: bool
        Whether to print headers
    sample_separator: str
        A separator to put between samples (optional)
    """
    if print_header:
        _print_alignments_global_header(
            file=file, empty_symbol=empty_symbol, separator=separator
        )
    for dets in details_by_utterance:
        if dets["scored"]:
            if print_header:
                _print_alignment_header(dets, file=file)
            _print_alignment(
                dets["alignment"],
                dets["ref_chars"],  # Changed from ref_tokens
                dets["hyp_chars"],  # Changed from hyp_tokens
                file=file,
                empty_symbol=empty_symbol,
                separator=separator,
            )
            if sample_separator:
                print(sample_separator, file=file)


def _print_alignments_global_header(
        file=sys.stdout, empty_symbol="<eps>", separator=" ; "
):
    print("=" * 80, file=file)
    print("ALIGNMENTS", file=file)
    print("", file=file)
    print("Format:", file=file)
    print("<utterance-id>, CER DETAILS", file=file)
    # Print the format with the actual print_alignment function, using artificial data:
    a = ["r", "e", "f", "e", "r", "e", "n", "c", "e"]
    b = ["h", "y", "p", "o", "t", "h", "e", "s", "i", "s"]
    alignment = [
        ('sub', 0, 0),
        ('eq', 1, 1),
        ('eq', 2, 2),
        ('del', 3, None),
        ('eq', 4, 3),
        ('eq', 5, 4),
        ('eq', 6, 5),
        ('eq', 7, 6),
        ('eq', 8, 7),
        ('ins', None, 8),
        ('ins', None, 9)
    ]
    _print_alignment(
        alignment,
        a,
        b,
        file=file,
        empty_symbol=empty_symbol,
        separator=separator,
    )



def _print_alignment(
        alignment, a, b, empty_symbol="<eps>", separator=" ; ", file=sys.stdout
):
    # First, get equal length text for all:
    a_padded = []
    b_padded = []
    ops_padded = []
    for op, i, j in alignment:  # i indexes a, j indexes b
        op_string = str(op)
        a_string = str(a[i]) if i is not None else empty_symbol
        b_string = str(b[j]) if j is not None else empty_symbol
        pad_length = max(len(op_string), len(a_string), len(b_string))
        a_padded.append(a_string.center(pad_length))
        b_padded.append(b_string.center(pad_length))
        ops_padded.append(op_string.center(pad_length))
    # Then print, in the order Ref, op, Hyp
    print(separator.join(a_padded), file=file)
    print(separator.join(ops_padded), file=file)
    print(separator.join(b_padded), file=file)

def _print_alignment_header(cer_details, file=sys.stdout):
    print("=" * 80, file=file)
    print(
        "{key}, %CER {CER:.2f} ]".format(
            **cer_details
        ),
        file=file,
    )

def _print_alignment(
    alignment, a, b, empty_symbol="<eps>", separator=" ; ", file=sys.stdout
):
    # First, get equal length text for all:
    a_padded = []
    b_padded = []
    ops_padded = []
    for op, i, j in alignment:  # i indexes a, j indexes b
        op_string = str(op)
        a_string = str(a[i]) if i is not None else empty_symbol
        b_string = str(b[j]) if j is not None else empty_symbol
        # NOTE: the padding does not actually compute printed length,
        # but hopefully we can assume that printed length is
        # at most the str len
        pad_length = max(len(op_string), len(a_string), len(b_string))
        a_padded.append(a_string.center(pad_length))
        b_padded.append(b_string.center(pad_length))
        ops_padded.append(op_string.center(pad_length))
    # Then print, in the order Ref, op, Hyp
    print(separator.join(a_padded), file=file)
    print(separator.join(ops_padded), file=file)
    print(separator.join(b_padded), file=file)


