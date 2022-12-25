import numpy as np
import matplotlib.pyplot as plt


def viterbi(sentence, states, emission_probs, trans_mat):
  '''
  Viterbi implementation of maximum a posteriori optimization for HMM model using dynamic programming.
  Returns most likely sequence of hidden states.
  Args:
      sentence: List[int], list of character id
      states: List[str], list of hidden states names
      emissions_probs: np.array, emission matrix (n_hidden, n_observed)
      trans_mat: np.array, transition matrix (n_hidden, n_hidden)
  Returns:
      sequence: List[int], list of hidden states id
  '''

  # compute the sentence length
  T = len(sentence)

  # compute the number of possible tags
  N = len(states)
   
  # create the dynamic program table (TxN array)
  V = np.zeros((T, N), np.float64)
   
  # create the backpointers dictionnary 
  B = np.zeros((T, N))
   
  # find the starting log probabilities for each state
  for i,hidden_state in enumerate(states):
    emit=emission_probs[i][sentence[0]]
    if emit==0:
      emit=0.0001
    V[0][i]=np.log(emit)

  # find the maximum log probabilities for reaching each state at time t
  for t in range(1,T):
    for i,hidden_state in enumerate(states):
      emit=emission_probs[i][sentence[t]]
      if emit==0:
        emit=0.00001

      all_paths=[]

      for j,prev_state in enumerate(states):
        transit=trans_mat[j][i]
        if transit==0:
          transit=0.00001
        all_paths.append(V[t-1][j] + np.log(emit) + np.log(transit))

      jj=np.argmax(all_paths)
      B[t][i] = jj
      V[t][i] = all_paths[jj]
          
  # find the highest probability final state
  m=max(V[T-1,:])
  final_state=np.where(V[T-1,:]==m)[0][0]

  sequence = []
  sequence.append(states[final_state])
   
  # traverse the back-pointers B to find the state sequence
  t=T-1
  current_state=final_state
  while t>0:
    prev_state=int(B[t][current_state])
    sequence.append(states[prev_state])
    current_state=prev_state
    t-=1

  return sequence[::-1]


def plot_parameters(states, trans_mat, emission_probs):
  ''' Inspect model parameters and visualize matrices'''

  plt.figure(1, figsize=(15,5))
  plt.subplot(121)
  plt.imshow(trans_mat, cmap="gray")
  plt.yticks(np.arange(len(states)), states)
  plt.title("Transition matrix {}".format(trans_mat.shape))
  #plt.colorbar()
  plt.subplot(122)
  plt.imshow(emission_probs, cmap="gray")
  plt.yticks(np.arange(len(states)), states)
  plt.title("Emission probs {}".format(emission_probs.shape))
  #plt.colorbar()
  plt.show()