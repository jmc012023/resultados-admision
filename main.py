import asyncio
from scraping import webpage_content as wp
from scraping import columns_wpcontent as cwp
from scraping import data_links as dl
from transform import clean as tc

async def main():
    ### web scraping part ###
    webpage_data = wp.create_webpage_data()
    print("PART 1 OF 4 IS DONE")
    print("PLEASE WAIT .....")

    ### clean data scraping part ###
    webpage_frame, initial_wp_frame = cwp.create_webpage_frame(webpage_data)
    initial_wp_frame.to_csv("./scraping/webpage_content.csv", index=False)
    webpage_frame.to_csv("./transform/cleaned_wp_content.csv", index=False)
    print("PART 2 OF 4 IS DONE")
    print("PLEASE WAIT .....")

    ### create frame by link of the all web data ###
    results_by_link_frame = await dl.join_data_links(webpage_frame[cwp.ResultColumnNames.LINK.value])
    results_by_link_frame.to_csv("./transform/results_by_links.csv", index=False)
    print("PART 3 OF 4 IS DONE")
    print("PLEASE WAIT .....")

    ### transform all data of links ###
    results = tc.create_results_frame(results_by_link_frame, webpage_frame)
    results.to_csv('unt_results.csv', index=False, encoding="utf-8")
    print(results)
    print("PART 4 OF 4 IS DONE")
    print("################# THE PROCESS HAS FINISHED ######################")

if __name__ == '__main__':
    asyncio.run(main())