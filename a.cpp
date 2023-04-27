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
  int array[10];
  for (int i = 0; i < n; i++)
    array[i] = rand() % 100 - 50;

  bubble_sort(array, n);

  for (int i = 0; i < n; i++) {
    cout << array[i] << " ";
  }

  return 0;
}

