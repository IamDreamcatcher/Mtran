void check(int n)
{
  n++;
  n--;
  double x = 0.12;
  int prime[n+1];
  for (int i = 0; i <= n; i++) {
	prime[i] = 0;
  }
  prime[0] = 1;
  prime[1] = 1;
  for (int i = 2; i <= n; i++) {
	if (prime[i] == 0) {
		if (i * i <= n){
			for (int j = i * i; j <= n; j += i) {
				prime[j] = 1;
			}
		}
	}
  }

  if (prime[n] == 0) {
  	cout << n << " is a prime number" << endl;
  }
  else {
	 cout << n << " is not a prime number" << endl;
  }
}

int main()
{
  int n = rand() % 100;
  check(n);

  return 0;
}