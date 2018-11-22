library("ggplot2")

names <- c("commons-lang", "jfreechart", "jodatime", "mockito")

suffixes <- c("-onefailingtest-filtering", "-allfailingtest-filtering", "-allfailingtest", "-onefailingtest")

for (name in names) {
    for (suffix in suffixes) {
        # loading file
        filename <- paste(name, suffix, sep="")
        mydata <- read.table(paste(filename, ".dat", sep=""), header=TRUE)
            
        # rendering plot
        p <- ggplot(mydata, aes(n, topn, group=slicing))+
        geom_step()+
        geom_point(aes(colour=slicing))+
        annotate("text",x=min(mydata$n)+30,y=min(mydata$topn)+2,hjust=.2,label=name)+
        scale_x_continuous(breaks = seq(min(mydata$n), max(mydata$n), 20), limits = c(min(mydata$n), max(mydata$n))) +
        # scale_y_continuous(breaks = seq(0, 100, 20), limits = c(0, 100)) +
        theme(legend.position=c(.9,.15)) +
        theme(axis.text.x = element_text(size=9))  +
        theme(axis.text.y = element_text(size=9))  
        
        
        p <- p + geom_vline(xintercept=10, color="red")

        # saving plot to file
        update_geom_defaults("point", list(size=1))
        theme_set(theme_grey(base_size=6))
        pdf(paste(filename, ".pdf", sep=""), width=3, height=2)
        print(p)
        graphics.off()
    }
}
