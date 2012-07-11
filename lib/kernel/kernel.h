#define cij(d1,d2,a,i,j) a[i*d2+j]
#define sij(d1,d2,a,i,j,s) a[i*d2+j]+=s

double gauss(double x, double A, double mu, double sigma );
double dgauss(double x, double A, double mu, double sigma );

// Gauss cutoff
#define CUTOFF 3
