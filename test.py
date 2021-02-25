from typing import Iterable

def find(data_structure:Iterable, *search, contains_some:bool  = False  ) -> bool:

  """
     Used to quickly see if data structure contains all or at least one value(s)
     if you want to see how many values where found then also return len(search) - result

    ------------------------------------------------------------------------
    Algorithm:

          1. search values are packed into tuple and converted to a set
          2. difference()  is applied and returns a set of whats found in search but not found in data_structure
          3. result is assigned the length of this new set which means how many values where not found
          4. if all values must be found then (result == 0 ) is returned
             if at least one value must be found then (result <= len(search)) is returned

    ------------------------------------ ------------------------------------

     Complexity:
          time:  O(1)
          space: O(1)

    ----------------------------------

   :param data_structure:
        a iterable data structure

   :param search:
        values that will be searched

   :param contains_some:
        a keyword only argument T/F = all values exist / at least one value exists

   :return:
        value(s) found or not found
  """

  # raises error if data_structure argument is not iterable
  iter(data_structure)

  # raises error if contains_some argument is not boolean
  assert(type(contains_some) == bool) , TypeError("contains_some argument must be boolean")

  result  = len(   set(search).difference(data_structure)   )


  return (result < len(search)) if contains_some else (result == 0)

i = None

print(type(i))












