|   | input a;  /* input for a is 7 */
|   | x = 0;
| | | j = 5;
| |   a = a - 10; /* should a = a + 10; */
| |   if (a > j) {
        x = x + 1;
      }
|     else {
|       z = 0;
|     }
| | | x = x + j;
| | | print x;   /* x is 5, but should be 6 */
