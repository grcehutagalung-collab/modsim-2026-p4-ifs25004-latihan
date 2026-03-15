#include <stdio.h>
#include <math.h>

int main() {

    // Parameter tangki
    float radius, tinggi_maks;
    float Qin, Qout;
    float A, volume = 0;
    float dt = 1;
    int waktu = 0;

    printf("Masukkan radius tangki (m): ");
    scanf("%f", &radius);

    printf("Masukkan tinggi maksimum tangki (m): ");
    scanf("%f", &tinggi_maks);

    printf("Masukkan debit masuk Qin (m3/detik): ");
    scanf("%f", &Qin);

    printf("Masukkan debit keluar Qout (m3/detik): ");
    scanf("%f", &Qout);

    // luas alas silinder
    A = M_PI * radius * radius;

    // volume maksimum
    float Vmax = A * tinggi_maks;

    printf("\nSimulasi perubahan tinggi air:\n");
    printf("Waktu(s)\tTinggi Air(m)\n");

    while(volume <= Vmax && volume >= 0) {

        float tinggi = volume / A;

        printf("%d\t\t%.2f\n", waktu, tinggi);

        // perubahan volume
        volume = volume + (Qin - Qout) * dt;

        waktu++;

        if(volume >= Vmax) {
            printf("\nTangki penuh pada waktu %d detik\n", waktu);
            break;
        }

        if(volume <= 0 && waktu > 0) {
            printf("\nTangki kosong pada waktu %d detik\n", waktu);
            break;
        }
    }

    // perhitungan waktu teoritis
    if(Qin > Qout){
        float waktu_penuh = Vmax / (Qin - Qout);
        printf("Perkiraan waktu tangki penuh: %.2f detik\n", waktu_penuh);
    }

    if(Qout > 0){
        float waktu_kosong = Vmax / Qout;
        printf("Perkiraan waktu tangki kosong: %.2f detik\n", waktu_kosong);
    }

    return 0;
}