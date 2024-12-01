"""Calculate accuracy.

Authors
* Jianyuan Zhong 2020
"""

import torch

from speechbrain.dataio.dataio import length_to_mask


def Accuracy(predicted_words,target_words,log_probabilities, targets, length=None):
    """Calculates the accuracy for predicted log probabilities and targets in a batch.

    Arguments
    ---------
    log_probabilities : torch.Tensor
        Predicted log probabilities (batch_size, time, feature).
    targets : torch.Tensor
        Target (batch_size, time).
    length : torch.Tensor
        Length of target (batch_size,).

    Returns
    -------
    numerator : float
        The number of correct samples
    denominator : float
        The total number of samples

    Example
    -------
    >>> probs = torch.tensor([[0.9, 0.1], [0.1, 0.9], [0.8, 0.2]]).unsqueeze(0)
    >>> acc = Accuracy(torch.log(probs), torch.tensor([1, 1, 0]).unsqueeze(0), torch.tensor([2/3]))
    >>> print(acc)
    (1.0, 2.0)
    """
    if length is not None:
        mask = length_to_mask(
            length * targets.shape[1],
            max_len=targets.shape[1],
        ).bool()
        if len(targets.shape) == 3:
            mask = mask.unsqueeze(2).repeat(1, 1, targets.shape[2])
    
    
    padded_pred = log_probabilities.argmax(-1)

    if length is not None:
        #Compare all the token in the target.
        if length[0] == 1:
            print("entered the isolated counter")
            if predicted_words[0] == target_words[0]:
                denominator = 1
                numerator = 1
            else:
                denominator = 1
                numerator = 0

        else:
            numerator = torch.sum(
                padded_pred.masked_select(mask) == targets.masked_select(mask)
            )
            denominator = torch.sum(mask)
    else:
        numerator = torch.sum(padded_pred == targets)
        denominator = targets.shape[1]
    return float(numerator), float(denominator)


class AccuracyStats:
    """Module for calculate the overall one-step-forward prediction accuracy.

    Example
    -------
    >>> probs = torch.tensor([[0.9, 0.1], [0.1, 0.9], [0.8, 0.2]]).unsqueeze(0)
    >>> stats = AccuracyStats()
    >>> stats.append(torch.log(probs), torch.tensor([1, 1, 0]).unsqueeze(0), torch.tensor([2/3]))
    >>> acc = stats.summarize()
    >>> print(acc)
    0.5
    """

    def __init__(self):
        self.correct = 0
        self.total = 0

    def append(self, predicted_words,target_words, log_probabilities, targets, length=None):
        """This function is for updating the stats according to the prediction
        and target in the current batch.

        Arguments
        ---------
        log_probabilities : torch.Tensor
            Predicted log probabilities (batch_size, time, feature).
        targets : torch.Tensor
            Target (batch_size, time).
        length : torch.Tensor
            Length of target (batch_size,).
        """
        numerator, denominator = Accuracy(predicted_words,target_words,log_probabilities, targets, length)
        self.correct += numerator
        self.total += denominator

    def summarize(self):
        """Computes the accuracy metric."""
        return self.correct / self.total
