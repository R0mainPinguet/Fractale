import imageio as iio

path = "C:\\Users\\R0MAIN\\Documents\\GitHub\\Fractale\\flames\\rendering techniques effects\\seed - 16 -- 1 3 8\\"

names = ["a - binary" , "b - linear" , "c - logarithmic" , "d - colors" , "e - gamma 4.0" ]
images = []

for name in names:
    images.append( iio.imread( path + name + ".png"  ))

#= Freeze on the last frame =#
for i in range(5):
    images.append( iio.imread( path + names[-1] + ".png"  ))

iio.mimsave(path + "0 - Compilation.gif", images , duration = 1)
