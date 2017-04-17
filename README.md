# Implementing an Audio Search Algorithm

This was the final project for MTH 438 - Numerical Analysis II taken at the University at Buffalo.  The work is a collaboration between me and two other students of the class, and the final write-up was written with a the project syllabus (now lost) in mind.

We were tasked with reproducing the algorthm used by software, such as Shazam, which is able to correctly identify songs recorded in low-resolution even in noisey environments.  The algorthm was implemented using low-level Python libraries such as Numpy, Scipy, and Pyplot.  We had to perform the necessary linear alegbra manipulation to the raw wav files without using any higher level Python libraries that may be available.  As a result, we had to learn and understand many fundamental concepts involved with signal processing, specifically focusing on Fourier transformations and their applications.  We also had to examine effecient hashing algorthms and optimization using vectorization.

The results of the project are optimistic, with a small test set yielding 100% accuracy.  In it's current state, the code isn't runable, and the only remaining assets of the project is the final write-up.  The included code is taken from the write-up, and might not run as-is.
