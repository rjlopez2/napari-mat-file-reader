import napari

# import myModule
# import importlib
# importlib.reload(myModule)
# from myModule import *

# t = 70
# print(t)
# viewer = napari.view_image(data.cells3d(), channel_axis=1, ndisplay=3)

# viewer.open("12h-49m-26s.sif", plugin="napari-"  )
viewer = napari.Viewer()
viewer.open("/Users/rubencito/programming_stuff/p_experimental/image_analysis/napari_play/OMAAS/test_data/11h-30m-01sTracked_CCSize8_StepSize4_ElementSize5_10fps.mat", plugin= "napari-mat-file-reader")


napari.run()  # start the "event loop" and show the viewer

print("end")