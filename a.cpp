void bubble_sort(int *array, int size) {

  for (int step = 0; step < size; step++) {
    for (int i = 0; i < size - step; i++) {
      if (array[i] > array[i + 1]) {
        int temp = array[i];
        array[i] = array[i + 1];
        array[i + 1] = temp;
      }
    }
  }
}

int main() {
  int n = 10;
  int array[10] = {1,2,3,4,5,6,7,8,9,10};
  for (int i = 0; i < n; i++)
    array[i] = rand() % 100 - 50;

  bubble_sort(array, n);

  for (int i = 0; i < n; i++) {
    cout << array[i] << " ";
  }

  return 0;
}



int main() {
  int n = 10;
  int array[5] = {1, 2, 3, 4, 5};
  int array2[5] = {1, 2, 3, 4, 5};
  int array3[10];
  int j = 0;
  for (int i = 0; i < 5; i++) {
    array3[j] = array[i];
    j++;
    array3[j] = array2[i];
    j++;
  }


  for (int i = 0; i < 10; i++) {
    cout << array3[i] << " ";
  }

  return 0;
}

