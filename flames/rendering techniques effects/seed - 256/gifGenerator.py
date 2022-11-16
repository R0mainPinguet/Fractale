import imageio as iio

path = "C:\\Users\\R0MAIN\\Documents\\GitHub\\Fractale\\flames\\rendering techniques effects\\seed - 256\\"

names = ["a - binary" , "b - linear" , "c - logarithmic" , "d - colors" , "e6 - good gamma 4" ]
images = []

for name in names:
    images.append( iio.imread( path + name + ".png"  ))

#= Freeze on the last frame =#
for i in range(5):
    images.append( iio.imread( path + names[-1] + ".png"  ))

iio.mimsave(path + "movie.gif", images , duration = 1)
