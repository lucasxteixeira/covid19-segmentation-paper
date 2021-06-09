seg <- c(0.83, 0.78, 0.83, 0.88, 0.87, 0.89, 0.9, 0.91, 0.92)
noseg <- c(0.94, 0.91, 0.86, 0.91, 0.9, 0.9, 0.91, 0.92, 0.91)

wilcox.test(seg, noseg, paired = TRUE, alternative = "two.sided")

t <- BayesFactor::ttestBF(seg, noseg, paired = TRUE)
bayestestR::describe_posterior(t)

df <- data.frame(
  id = c(1:9, 1:9),
  model = rep(c("VGG16", "ResNet50V2", "InceptionV3"), 3),
  y = c(seg, noseg),
  x = c(rep("Segmented", 9), rep("Non-segmented", 9))
)

library(ggplot2)
library(ggpirate)


ggplot(df, aes(x,y)) +
  geom_violin(aes(fill = factor(x)), color = NA) +
  geom_point(aes(group = id), alpha = 0.2) +
  geom_line(aes(group = id), alpha = 0.2) +
  stat_summary(fun.data = "mean_cl_normal", size = 2, geom = "point", alpha = 0.6) +
  stat_summary(fun.y = "mean", size = 1, geom = "line", aes(group = 1), alpha = 0.6) +
  xlab("") + ylab("F1-Score") +
  see::theme_modern() + see::scale_color_material() + see::scale_fill_material() +
  scale_fill_manual(values=c("#F45E42", "#FFA392")) +
  theme(legend.position = "none")


ggplot(df, aes(x = x, y = y)) +
  geom_pirate(aes(colour = x), bars = FALSE,
              points_params = list(shape = 19, alpha = 0.2),
              lines_params = list(size = 0.8)) +
  see::theme_modern() + see::scale_color_material() + see::scale_fill_material() +
  xlab("") + ylab("F1-Score") +
  theme(axis.text.x = element_text(color = "grey20", size = 15, angle = 0, hjust = .5, vjust = .5, face = "plain"),
        axis.text.y = element_text(color = "grey20", size = 15, angle = 0, hjust = 1, vjust = 0, face = "plain"),
        axis.title.x = element_text(color = "grey20", size = 12, angle = 0, hjust = .5, vjust = 0, face = "plain"),
        axis.title.y = element_text(color = "grey20", size = 15, angle = 90, hjust = .5, vjust = .5, face = "plain"))

ggsave("violin-segment.png", width = 10, height = 8, dpi = 300)

ggplot(df, aes(x = model, y = y)) +
  geom_pirate(aes(colour = model), bars = FALSE,
              points_params = list(shape = 19, alpha = 0.2),
              lines_params = list(size = 0.8)) +
  see::theme_modern() + see::scale_color_material() + see::scale_fill_material() +
  xlab("") + ylab("F1-Score") +
  theme(axis.text.x = element_text(color = "grey20", size = 15, angle = 0, hjust = .5, vjust = .5, face = "plain"),
        axis.text.y = element_text(color = "grey20", size = 15, angle = 0, hjust = 1, vjust = 0, face = "plain"),
        axis.title.x = element_text(color = "grey20", size = 12, angle = 0, hjust = .5, vjust = 0, face = "plain"),
        axis.title.y = element_text(color = "grey20", size = 15, angle = 90, hjust = .5, vjust = .5, face = "plain"))

ggsave("violin-models.png", width = 10, height = 8, dpi = 300)

ggplot(df, aes(x = model, y = y)) +
  facet_wrap(~x) +
  geom_pirate(aes(colour = model), bars = FALSE,
              points_params = list(shape = 19, alpha = 0.2),
              lines_params = list(size = 0.8)) +
  see::theme_modern() + see::scale_color_material() + see::scale_fill_material() +
  xlab("") + ylab("F1-Score") +
  theme(strip.text.x = element_text(color = "grey20", size = 15, angle = 0, hjust = .5, vjust = .5, face = "plain"),
        axis.text.x = element_text(color = "grey20", size = 15, angle = 30, hjust = .5, vjust = .5, face = "plain"),
        axis.text.y = element_text(color = "grey20", size = 15, angle = 0, hjust = 1, vjust = 0, face = "plain"),
        axis.title.x = element_text(color = "grey20", size = 12, angle = 0, hjust = .5, vjust = 0, face = "plain"),
        axis.title.y = element_text(color = "grey20", size = 15, angle = 90, hjust = .5, vjust = .5, face = "plain"))

ggsave("violin-segment-models.png", width = 10, height = 8, dpi = 300)