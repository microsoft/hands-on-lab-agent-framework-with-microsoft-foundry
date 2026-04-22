There is an issue with the Azure App Services is causing intermittent 500 errors. 
                        Traceback (most recent call last):
                                    File "<string>", line 38, in <module>
                                        main_application()                    ← Entry point
                                    File "<string>", line 30, in main_application
                                        results = process_data_batch(test_data)  ← Calls processor
                                    File "<string>", line 13, in process_data_batch
                                        avg = calculate_average(batch)        ← Calls calculator
                                    File "<string>", line 5, in calculate_average
                                        return total / count                  ← ERROR HERE
                                            ~~~~~~^~~~~~~
                                    ZeroDivisionError: division by zero