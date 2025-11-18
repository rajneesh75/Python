import gc

gc.collect()  # Force a garbage collection cycle
print(gc.get_count())  # View current GC thresholds
